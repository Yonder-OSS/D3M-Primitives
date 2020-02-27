from d3m import index
from d3m.metadata.base import ArgumentType
from d3m.metadata.pipeline import Pipeline, PrimitiveStep

# Creating pipeline
pipeline_description = Pipeline()
pipeline_description.add_input(name="inputs")

# Step 0: DS to DF on input DS
step_0 = PrimitiveStep(
    primitive=index.get_primitive(
        "d3m.primitives.data_transformation.dataset_to_dataframe.Common"
    )
)
step_0.add_argument(
    name="inputs", argument_type=ArgumentType.CONTAINER, data_reference="inputs.0"
)
step_0.add_output("produce")
pipeline_description.add_step(step_0)

# Step 1: Simple Profiler Column Role Annotation
step_1 = PrimitiveStep(
    primitive=index.get_primitive("d3m.primitives.schema_discovery.profiler.Common")
)
step_1.add_argument(
    name="inputs",
    argument_type=ArgumentType.CONTAINER,
    data_reference="steps.0.produce",
)
step_1.add_output("produce")
pipeline_description.add_step(step_1)

# Step 2: column parser on input DF
step_2 = PrimitiveStep(
    primitive=index.get_primitive(
        "d3m.primitives.data_transformation.column_parser.Common"
    )
)
step_2.add_argument(
    name="inputs",
    argument_type=ArgumentType.CONTAINER,
    data_reference="steps.1.produce",
)
step_2.add_output("produce")
step_2.add_hyperparameter(
    name="parse_semantic_types",
    argument_type=ArgumentType.VALUE,
    data=[
        "http://schema.org/Boolean",
        "http://schema.org/Integer",
        "http://schema.org/Float",
        "https://metadata.datadrivendiscovery.org/types/FloatVector",
        "http://schema.org/DateTime",
    ],
)
pipeline_description.add_step(step_2)

# Step 3: parse attribute and index semantic types
step_3 = PrimitiveStep(
    primitive=index.get_primitive(
        "d3m.primitives.data_transformation.extract_columns_by_semantic_types.Common"
    )
)
step_3.add_argument(
    name="inputs",
    argument_type=ArgumentType.CONTAINER,
    data_reference="steps.2.produce",
)
step_3.add_hyperparameter(
    name="semantic_types",
    argument_type=ArgumentType.VALUE,
    data=[
        "https://metadata.datadrivendiscovery.org/types/Attribute",
        "https://metadata.datadrivendiscovery.org/types/PrimaryKey",
    ],
)
step_3.add_output("produce")
pipeline_description.add_step(step_3)

# Step 4: parse target semantic types
step_4 = PrimitiveStep(
    primitive=index.get_primitive(
        "d3m.primitives.data_transformation.extract_columns_by_semantic_types.Common"
    )
)
step_4.add_argument(
    name="inputs",
    argument_type=ArgumentType.CONTAINER,
    data_reference="steps.2.produce",
)
step_4.add_hyperparameter(
    name="semantic_types",
    argument_type=ArgumentType.VALUE,
    data=[
        "https://metadata.datadrivendiscovery.org/types/Target",
    ],
)
step_4.add_output("produce")
pipeline_description.add_step(step_4)

# Step 5: forecasting primitive
step_5 = PrimitiveStep(
    primitive=index.get_primitive(
        "d3m.primitives.time_series_forecasting.vector_autoregression.VAR"
    )
)
step_5.add_argument(
    name="inputs",
    argument_type=ArgumentType.CONTAINER,
    data_reference="steps.3.produce",
)
step_5.add_argument(
    name="outputs",
    argument_type=ArgumentType.CONTAINER,
    data_reference="steps.4.produce",
)
step_5.add_output("produce")
pipeline_description.add_step(step_5)

# Final Output
pipeline_description.add_output(
    name="output predictions", data_reference="steps.5.produce"
)

# Output json pipeline
blob = pipeline_description.to_json()
filename = blob[8:44] + ".json"
# filename = "pipeline.json"
with open(filename, "w") as outfile:
    outfile.write(blob)
