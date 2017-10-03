# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 14:30:14 2017
metric_calculations
A module for functions that will calculate useful metrics (e.g. false positive
and true positive rates)
@author: Tom Wakeford
"""
import pandas as pd
import numpy as np


# Calculates the true positive rate and false positive rate
# for each unique score in the input dataframe
# df: a dataframe with columns 'class' and 'score'
# fp_cost: a numeric value for the cost of a single false positive
# fn_cost: a numeric value for the cost of a single false negative
# returns roc_df, a dataframe with columns 'threshold', 'TPR', 'FPR', 'cost'
def build_roc_data(df, fp_cost=1, fn_cost=1):
    roc_list = []
    # Use the unique list of scores as a set of thresholds
    threshold_set = set(df['score'])
    # Make sure that we include 0 and 1
    threshold_set.update([0, 1])
    for threshold in threshold_set:
        tp, fp, tn, fn = confusion_matrix(df, threshold)
        cost = (fp * fp_cost) + (fn * fn_cost)
        tpr = tp / (tp + fn)
        fpr = fp / (fp + tn)
        roc_list.append([threshold, tpr, fpr, cost])
    roc_df = pd.DataFrame(roc_list, columns=['threshold', 'TPR', 'FPR', 'cost'])
    roc_df.sort_values(by='threshold', inplace=True)
    return roc_df


# Calculates the true positive rate and false positive rate
# for each unique score in the input dataframe
# df: a dataframe with columns 'class' and 'score'
# returns roc_df, a dataframe with columns 'threshold', 'TPR', 'FPR'
def build_roc_data_intervals(df, threshold_set=np.arange(0, 1, .01), fp_cost=1, fn_cost=1):
    roc_list = []
    for threshold in threshold_set:
        tp, fp, tn, fn = confusion_matrix(df, threshold)
        cost = (fp * fp_cost) + (fn * fn_cost)
        tpr = tp / (tp + fn)
        fpr = fp / (fp + tn)
        roc_list.append([threshold, tpr, fpr, cost])
    roc_df = pd.DataFrame(roc_list, columns=['threshold', 'TPR', 'FPR', 'cost'])
    roc_df.sort_values(by='threshold', inplace=True)
    return roc_df

def build_roc_data_fast(df_input, fp_cost=1, fn_cost=1):
    
    df = df_input[['score', 'class']].copy()
    df.columns = ['threshold', 'class']
    df['not_class'] = 1 - df['class']
    
    df = df.groupby(['threshold']).sum().reset_index(False)
    df.sort_values(by='threshold', ascending=True, inplace=True)    
    
    p_count = df['class'].sum()
    n_count = df['not_class'].sum()
    
    df['FN'] = df['class'].cumsum() - df['class']
    df['TN'] = df['not_class'].cumsum() - df['not_class']
    df['TP'] = p_count - df['FN']
    df['FP'] = n_count - df['TN']    

    df['TPR'] = df['TP'] / (df['TP'] + df['FN'])
    df['FPR'] = df['FP'] / (df['FP'] + df['TN'])
    df['cost'] = df['FP'] * fp_cost + df['FN'] * fn_cost
    
    return df[['threshold', 'TP', 'FN', 'TN', 'FP', 'TPR', 'FPR', 'cost']]

# Calculates the elements of the confusion matrix
# df: a dataframe with columns 'class' and 'score'
# 'class' is 0/1 for the negative/positive class respectively
# threshold: scores below the threshold are negative, above or equal to the threshold are positive
# returns a tuple of counts: true positive, false positive, true negative, false negative
def confusion_matrix(df, threshold):
    # A slice containing records scored as positive (i.e. above the threshold)
    positive_df = df[df['score'] >= threshold]
    # A slice containing records scored as negative (i.e. below the threshold)    
    negative_df = df[df['score'] < threshold]

    # True positives have been scored positive and really are positive
    tp_count = positive_df[positive_df['class'] == 1].shape[0]
    # False positive have been scored positive but aren't really 
    fp_count = positive_df[positive_df['class'] == 0].shape[0]
    # True negatives have been scored negative and really are negative
    tn_count = negative_df[negative_df['class'] == 0].shape[0]
    # False negatives have been scored negative but aren't really
    fn_count = negative_df[negative_df['class'] == 1].shape[0]

    return tp_count, fp_count, tn_count, fn_count
