from lib.transformer import Transformer

transformer = Transformer()
transformer.transform_content_hostname(
    "data/Degreed_ExampleCompletions.csv",
    "data/Degreed_Transformed_Completions.csv",
)