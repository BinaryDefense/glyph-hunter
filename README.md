# glyph-hunter
Python Flask web app that checks names for potential homoglyph characteristics and reports results in json format

# Installation
Set up Python3 virtual environment, install requirements from requirements.txt, and set up a reverse proxy of your choice, such as nginx to handle TLS connections and route requests to the Flask app. It is recommended to use gunicorn to handle connections between nginx and Flask.

# Queries
Submit potential homoglyph names to check via the "name" parameter of the "check" endpoint, like this:

https://your-domain-here.com/check?name=Aԁmіnistratοr

If you wish to specifically check name for similarity to other names, you may also submit the list of other names separated by double pipe characters (||) as a logical OR:

https://your-domain-here.com/check?name=Aԁmіnistratοr&other_names=Administrator||Admin||something-else

# Output
```
{
    "results":[
        {
            "existing_name":"Administrator",
            "homoglyph_score":1.0,
            "name_is_as_it_seems":false,
            "new_name":"A\u0501m\u0456nistrat\u03bfr",
            "non_ascii_characters":"['\u0501', '\u0456', '\u03bf']",
            "num_non_ascii_characters":3,
            "ocr_of_new_name":"Administrator",
            "ocr_similarity_to_new_name":0.7692307692307693
        },
        {
            "existing_name":"Admin",
            "homoglyph_score":0.5555555555555556,
            "name_is_as_it_seems":false,
            "new_name":"A\u0501m\u0456nistrat\u03bfr",
            "non_ascii_characters":"['\u0501', '\u0456', '\u03bf']",
            "num_non_ascii_characters":3,
            "ocr_of_new_name":"Administrator",
            "ocr_similarity_to_new_name":0.769230769230769
        }
    ]
}
```
