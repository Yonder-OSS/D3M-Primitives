from setuptools import setup, find_packages

setup(
    name="yonder-primitives",
    version="2.0.0",
    description="All Yonder primitives as a single library",
    packages=find_packages(),
    setkeywords=['d3m_primitive'],
    install_requires=[
        "numpy>=1.15.4,<=1.17.3",
        "scipy>=1.2.1,<=1.3.1",
        "scikit-learn[alldeps]>=0.20.3,<=0.21.3",
        "pandas>=0.23.4,<=0.25.2",
        "tensorflow-gpu == 2.0.0",
        "tslearn == 0.2.5",
        "statsmodels==0.10.2",
        "pmdarima==1.0.0",
        "punk==3.0.0",
        "deepar @ git+https://github.com/NewKnowledge/deepar@c801332d26742c17c4265d2155372ce7f1192bc4#egg=deepar-0.0.2",
        "object_detection_retinanet @ git+https://github.com/NewKnowledge/object-detection-retinanet@beca7ff86faa2295408e46fe221a3c7437cfdc81#egg=object_detection_retinanet"
        "Simon @ git+https://github.com/NewKnowledge/simon@fe41f4eb4f3af848841b325323fc7fc01cd7711b#egg=Simon-1.2.4",
        "hdbscan==0.8.25",
        "Simon @ git+https://github.com/NewKnowledge/simon@997a6a78a6bf920f05e68be6a052adf1348acce6#egg=Simon-1.2.4",
        "requests>=2.19.1,<=2.22.0",
        "nk_sent2vec @ git+https://github.com/NewKnowledge/nk-sent2vec@85cdd7538c41ea8edf49d15ab749d258656eff00#egg=nk_sent2vec",
        "shap == 0.34.0",
    ],
    entry_points={
        "d3m.primitives": [
            "data_cleaning.column_type_profiler.Simon = primitives.data_preprocessing.data_typing.wrapper:SimonPrimitive",
            "data_cleaning.geocoding.Goat_forward = primitives.data_preprocessing.geocoding_forward.forward:GoatForwardPrimitive",
            "data_cleaning.geocoding.Goat_reverse = primitives.data_preprocessing.geocoding_reverse.reverse:GoatReversePrimitive",
            "feature_extraction.nk_sent2vec.Sent2Vec = primitives.natural_language_processing.sent2vec.wrapper:Sent2VecPrimitive",
            "clustering.k_means.Sloth = primitives.clustering.k_means.Storc:StorcPrimitive",
            "clustering.hdbscan.Hdbscan = primitives.clustering.hdbscan.Hdbscan:HdbscanPrimitive",
            "clustering.spectral_graph_clustering.SpectralClustering = primitives.clustering.spectral_clustering.SpectralClustering:SpectralClusteringPrimitive",
            "dimensionality_reduction.t_distributed_stochastic_neighbor_embedding.Tsne = primitives.dimensionality_reduction.tsne.Tsne:TsnePrimitive",
            "time_series_classification.k_neighbors.Kanine = primitives.ts_classification.knn.classification_knn:KaninePrimitive",
            "time_series_forecasting.vector_autoregression.VAR = primitives.ts_forecasting.vector_autoregression.forecasting_var:VarPrimitive",
            "time_series_classification.convolutional_neural_net.LSTM_FCN = primitives.ts_classification.lstm_fcn.classification_lstm:LstmFcnPrimitive",
            "time_series_forecasting.lstm.DeepAR = primitives.ts_forecasting.deep_ar.forecasting_deepar:DeepArPrimitive",
            "object_detection.retinanet = primitives.object_detection.retinanet.object_detection_retinanet:ObjectDetectionRNPrimitive",
            "data_cleaning.data_cleaning.Datacleaning = primitives.data_preprocessing.data_cleaning.data_cleaning:DataCleaningPrimitive",
            "data_cleaning.text_summarization.Duke = primitives.data_preprocessing.duke.duke:DukePrimitive",
            "feature_selection.pca_features.Pcafeatures = primitives.feature_selection.pca_features.pca_features:PcaFeaturesPrimitive",
            "feature_selection.rffeatures.Rffeatures = primitives.feature_selection.rf_features.rf_features:RfFeaturesPrimitive"
            "classification.inceptionV3_image_feature.Gator = primitives.image_classification.imagenet_transfer_learning.gator:GatorPrimitive",
           
        ],
    },
)
