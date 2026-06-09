from models.parameter import Parameter

class ParameterExtractor:
    def extract(self, catia_document) -> dict[str, Parameter]:
        extracted_parameters = {}

        try:
            parameters = catia_document.Parameters
        except Exception as error:
            print(f"Failed to access parameters: {error}")
            return extracted_parameters
        
        for index in range(1, parameters.Count + 1):
            try:
                parameter = parameters.Item(index)

                parameter_name = parameter.Name
                try:
                    parameter_value = parameter.Value
                except Exception:
                    parameter_value = None
                
                extracted_parameters[parameter_name] = Parameter(
                    name = parameter_name,
                    value=str(parameter_value) if parameter_value is not None else None
                )
            except Exception as error:
                print(f"Failed to extrat parameter #{index}: {error}")

        return extracted_parameters