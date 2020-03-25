from d3m import index
from d3m.metadata.base import ArgumentType, Context
from d3m.metadata.pipeline import Pipeline, PrimitiveStep
import sys
# Creating pipeline
pipeline_description = Pipeline()
pipeline_description.add_input(name='inputs')

# Step 0: dataset_to_dataframe
step_0 = PrimitiveStep(primitive=index.get_primitive('d3m.primitives.data_transformation.dataset_to_dataframe.Common'))
step_0.add_argument(name='inputs', argument_type=ArgumentType.CONTAINER, data_reference='inputs.0')
step_0.add_output('produce')
pipeline_description.add_step(step_0)

# Step 1: Column profiler
step_1 = PrimitiveStep(primitive=index.get_primitive('d3m.primitives.schema_discovery.profiler.Common'))
step_1.add_argument(name='inputs', argument_type=ArgumentType.CONTAINER, data_reference='steps.0.produce')
step_1.add_output('produce')
pipeline_description.add_step(step_1)

# Step 2: column_parser
step_2 = PrimitiveStep(primitive=index.get_primitive('d3m.primitives.data_transformation.column_parser.Common'))
step_2.add_argument(name='inputs', argument_type=ArgumentType.CONTAINER, data_reference='steps.1.produce')
step_2.add_output('produce')
pipeline_description.add_step(step_2)

# Step 3: imputer
step_3 = PrimitiveStep(primitive=index.get_primitive('d3m.primitives.data_cleaning.imputer.SKlearn'))
step_3.add_argument(name='inputs', argument_type=ArgumentType.CONTAINER, data_reference='steps.2.produce')
step_3.add_output('produce')
step_3.add_hyperparameter(name='return_result', argument_type=ArgumentType.VALUE,data='replace')
step_3.add_hyperparameter(name='use_semantic_types', argument_type=ArgumentType.VALUE,data=True)
pipeline_description.add_step(step_3)

# Step 4: DISTIL/NK random forest feature selection
step_4 = PrimitiveStep(primitive=index.get_primitive('d3m.primitives.feature_selection.rffeatures.Rffeatures'))
step_4.add_argument(name='inputs', argument_type=ArgumentType.CONTAINER, data_reference='steps.3.produce')
step_4.add_argument(name='outputs', argument_type=ArgumentType.CONTAINER, data_reference='steps.3.produce')
step_4.add_output('produce')
step_4.add_hyperparameter(name='only_numeric_cols', argument_type=ArgumentType.VALUE,data=True)
step_4.add_hyperparameter(name='proportion_of_features', argument_type=ArgumentType.VALUE,data=1.0)
pipeline_description.add_step(step_4)

# Step 5: random_forest
step_5 = PrimitiveStep(primitive=index.get_primitive('d3m.primitives.classification.random_forest.SKlearn'))
step_5.add_argument(name='inputs', argument_type=ArgumentType.CONTAINER, data_reference='steps.4.produce')
step_5.add_argument(name='outputs', argument_type=ArgumentType.CONTAINER, data_reference='steps.4.produce')
step_5.add_output('produce')
step_5.add_hyperparameter(name='add_index_columns', argument_type=ArgumentType.VALUE,data=True)
step_5.add_hyperparameter(name='use_semantic_types', argument_type=ArgumentType.VALUE,data=True)
pipeline_description.add_step(step_5)

# Step 6: construct output
step_6 = PrimitiveStep(primitive=index.get_primitive('d3m.primitives.data_transformation.construct_predictions.Common'))
step_6.add_argument(name='inputs', argument_type=ArgumentType.CONTAINER, data_reference='steps.5.produce')
step_6.add_argument(name='reference', argument_type=ArgumentType.CONTAINER, data_reference='steps.0.produce')
step_6.add_output('produce')
pipeline_description.add_step(step_6)

# Final Output
pipeline_description.add_output(name='output predictions', data_reference='steps.6.produce')

# Output json pipeline
blob = pipeline_description.to_json()
filename = blob[8:44] + '.json'
#filename = 'rffeatures_pipeline.json'
with open(filename, 'w') as outfile:
    outfile.write(blob)
