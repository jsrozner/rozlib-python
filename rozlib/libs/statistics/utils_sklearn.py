import numpy as np
from sklearn.svm import SVC


def fit_svm(X_umap, y):
    """
    Fit an SVM classifier for a umap input
    Args:
        X_umap:
        y:

    Returns:

    """
    # Train SVM Classifier
    svm = SVC(kernel="linear", random_state=42)
    svm.fit(X_umap, y)

    # # Compute Decision Boundary
    # xx, yy = np.meshgrid(np.linspace(X_umap[:, 0].min() - 1, X_umap[:, 0].max() + 1, 100),
    #                      np.linspace(X_umap[:, 1].min() - 1, X_umap[:, 1].max() + 1, 100))

    # Create a finer, closer mesh grid
    x_min, x_max = X_umap[:, 0].min() - 0.2, X_umap[:, 0].max() + 0.2  # Reduce padding
    y_min, y_max = X_umap[:, 1].min() - 0.2, X_umap[:, 1].max() + 0.2

    xx, yy = np.meshgrid(
        np.linspace(x_min, x_max, 200),  # Increase grid resolution
        np.linspace(y_min, y_max, 200)
    )

    Z = svm.decision_function(np.c_[xx.ravel(), yy.ravel()])  # Compute decision values
    Z = Z.reshape(xx.shape)  # Reshape to match grid shape

    return xx, yy, Z
