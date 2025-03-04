import random

from sklearn.metrics import precision_score, recall_score, f1_score


def get_prf1(labels, y_pred):
    precision = precision_score(labels, y_pred)
    recall = recall_score(labels, y_pred)
    f1 = f1_score(labels, y_pred)
    return precision, recall, f1

def sample_evenly(labels, second_list, num_samples):
    """
    Given a List of binary labels (0 or 1), resample from labels and from second_list
    to give num_samples total, but with balance

    Could be used, e.g., for [labels, scores] or for [labels, preds]
    """

    labels_negative_idx = [i for i, l in enumerate(labels) if l == 0]
    print(len(labels_negative_idx))
    labels_positive_idx = [i for i, l in enumerate(labels) if l == 1]
    print(len(labels_positive_idx))

    # sample 50/50
    samples_pos = random.choices(range(len(labels_positive_idx)), k=num_samples)
    label_indexes_pos = [labels_positive_idx[i] for i in samples_pos]
    samples_neg = random.choices(range(len(labels_negative_idx)), k=num_samples)
    label_indexes_neg = [labels_negative_idx[i] for i in samples_neg]

    all_sample_idxs = label_indexes_pos + label_indexes_neg

    sampled_labels = [labels[i] for i in all_sample_idxs]
    sampled_scores = [second_list[i] for i in all_sample_idxs]
    return sampled_labels, sampled_scores
