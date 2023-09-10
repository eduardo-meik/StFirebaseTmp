#json-to-toml.py
import toml

output_file = ".streamlit/secrets.toml"

with open(".streamlit\pullmai-e0bb0-firebase-adminsdk-6nr9p-334c8b1770.json") as json_file:
    json_text = json_file.read()

config = {"textkey": json_text}
toml_config = toml.dumps(config)

with open(output_file, "w") as target:
    target.write(toml_config)