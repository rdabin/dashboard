import pandas as pd
import numpy as np


def create_sample_datafile(num_records=1000, filename='data/data.csv'):
    df = create_sample_df(num_records)
    df.to_csv(filename, index_label='id')


def create_sample_df(num_records=1000):
    """
    Create a sample testdataset mimicking output from a binary classifier.
    Assumes presence of multiple subgroups within dataset each of which may see a different distribution of scores
    for both class 0 and class 1.
    :param num_records: number of fake records to generate in dummy test dataset
    :return: a dataframe with columns ['id', 'group', 'classification', 'score']
    """

    np.random.seed(24)

    # Setting parameters for each group in population.
    num_groups = 2

    prevalance_of_subgroup_in_population = [.7, .3]
    assert len(prevalance_of_subgroup_in_population) == num_groups
    assert sum(prevalance_of_subgroup_in_population) == 1

    probability_of_class_1 = [.5, .2]
    assert len(probability_of_class_1) == num_groups

    # Dummy scores sampled from Beta distributions, with different alpha/beta params for each group (dim 0) and
    # true classification (dim 1)
    score_alpha = np.array([[2, 3],
                            [1, 2]])
    score_beta = np.array([[5, 1],
                           [3, 1.5]])
    assert score_alpha.shape == score_beta.shape == (num_groups, 2)

    # randomly sample each record from one of the groups
    prevalance_cumsum = np.cumsum(prevalance_of_subgroup_in_population)
    group_index = np.digitize(np.random.uniform(0, 1, size=num_records), prevalance_cumsum)
    assert group_index.shape == (num_records,)

    # choose random classification according to selected group
    classification_array = (np.random.uniform(0, 1, size=(num_records, num_groups)) < probability_of_class_1) * 1
    assert classification_array.shape == (num_records, num_groups)
    classification = classification_array[range(num_records), group_index]
    assert classification.shape == (num_records,)

    # choose random score according to selected group and true classification
    score_array = np.random.beta(score_alpha, score_beta, [num_records, num_groups, 2])
    assert score_array.shape == (num_records, num_groups, 2)
    score = score_array[range(num_records), group_index, classification]
    assert classification.shape == (num_records,)

    df = pd.DataFrame({'group': group_index,
                       'class': classification,
                       'score': score})

    return df


if __name__ == '__main__':
    create_sample_datafile()
    print(create_sample_df())
