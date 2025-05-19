TASKS_META = {
    "classification": {
        "label": "Classification",
        "hyperparams": {
            "n_estimators": {
                "type": "number", "label": "Trees", "default": 100, "min": 10, "max": 500
            },
            "max_depth": {
                "type": "number", "label": "Max Depth", "default": None, "min": 1, "max": 50
            },
            "criterion": {
                "type": "select", "label": "Criterion",
                "options": ["gini", "entropy"], "default": "gini"
            }
        }
    },
    "regression": {
        "label": "Regression",
        "hyperparams": {
            "n_estimators": {
                "type": "number", "label": "Trees", "default": 100, "min": 10, "max": 500
            },
            "max_depth": {
                "type": "number", "label": "Max Depth", "default": None, "min": 1, "max": 50
            },
            "criterion": {
                "type": "select", "label": "Criterion",
                "options": ["squared_error", "absolute_error"], "default": "squared_error"
            }
        }
    },
    "clustering": {
        "label": "Clustering",
        "hyperparams": {
            "n_clusters": {
                "type": "number", "label": "Clusters", "default": 3, "min": 2, "max": 20
            },
            "init": {
                "type": "select", "label": "Init",
                "options": ["k-means++", "random"], "default": "k-means++"
            },
            "max_iter": {
                "type": "number", "label": "Max Iter", "default": 300, "min": 100, "max": 1000
            }
        }
    }
}
