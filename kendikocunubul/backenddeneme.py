from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    # Render the HTML form
    return render_template('deneme4.html')  # Ensure 'form.html' is in the 'templates' directory.


# Specific values or messages for numerical questions
numerical_question_values = {
    1: "-Okulun çalışma temponuzdaki yeri",
    2: "-Dershanenin çalışma temponuzdaki yeri",
    3: "-Özel dersin çalışma temponuzdaki yeri",
    4: "-Youtube'daki Yks ders kanallarının çalışma temponuzdaki yeri",
    5: "-Hafta içerisindeki güncel çalışma düzeni"
 
    # ... and so on for each numerical question
}

# Specific values or messages for string-type questions
string_question_values = {
    1: "*ikiniz de aynı alandan sınava hazırlanıyorsunuz.",
    2: "*Değişken1.",
    3: "*Koçumuzun okuduğu üniversite ile hedeflediğiniz üniversite aynı.",
    4: "*Koçumuzun okuduğu bölüm ile hedeflediğiniz bölüm aynı.",
    5: "*İkiniz de en çok aynı derste zorluk çekiyorsunuz.",

    
    # ... and so on for each string-type question
}

class UserData:
    def __init__(self):
        self.name = "Test User"
        
        # Initialize attributes for numerical answers
        self.answer1 = 1
        self.answer2 = 1
        self.answer3 = 1
        self.answer4 = 1
        self.answer5 = 1
        
        # Initialize attributes for string-type answers
        self.string_answer1 = 'A'
        self.string_answer2 = 'A'
        self.string_answer3 = 'A'
        self.string_answer4 = 'A'
        self.string_answer5 = 'A'

    def update_from_form(self, form_data):
        self.name = form_data.get('name', self.name)

        # Update numerical answers
        for i in range(1, 6):
            answer_key = f'answer{i}'
            try:
                answer = int(form_data.get(answer_key, 0))
                setattr(self, answer_key, answer)
            except ValueError:
                setattr(self, answer_key, 0)

        # Update string-type answers
        for i in range(1, 6):
            string_answer_key = f'string_answer{i}'
            string_answer = form_data.get(string_answer_key, '')
            setattr(self, string_answer_key, string_answer)

class OptionData:
    def __init__(self):
        self.urls = {
            'Gül': 'https://shop.kantakademi.com/products/gul-rana',
            'Eleya': 'https://shop.kantakademi.com/products/eleya-ovul',
            'Rüya': 'https://shop.kantakademi.com/products/ruya'
        }
        self.stock_data = {'Gül': 2, 'Eleya': 2, 'Rüya': 2}
        self.preview_image_urls = {
            'Gül': 'https://shop.kantakademi.com/cdn/shop/products/1EeoN_LzlHrnOd2LnUq9Ujt3kvnGtxvw5.jpg?v=1700439401&width=600',
            'Eleya': 'https://shop.kantakademi.com/cdn/shop/files/EleyaOvulMadak.jpg?v=1698185012&width=600',
            'Rüya': 'https://shop.kantakademi.com/cdn/shop/products/12yFqoDWkeVOHXwDCk3PJZ3sJ5SzaENVi.jpg?v=1700439387&width=360'
        }

        # Numerical question values for each option
        self.numerical_values = {
            'Gül': [1, 1, 1, 1, 1],
            'Eleya': [3, 4, 5, 1, 2],
            'Rüya': [5, 5, 5, 5, 5]
        }

        # String-type question values for each option
        self.string_values = {
            'Gül': ['A', 'A', 'B', 'C', 'D'],
            'Eleya': ['A', 'B', 'C', 'D', 'A'],
            'Rüya': ['A', 'C', 'B', 'D', 'A']
        }


def calculate_best_option(user_data, option_data):
    option_scores = {}
    option_matching_details = {}  # Tracks details for each option
    
    for option, numerical_values in option_data.numerical_values.items():
        score = 0
        matching_details = []  # List to store detailed matching information

        # Check the crucial string-type question first
        if getattr(user_data, 'string_answer1') != option_data.string_values[option][0]:
            continue  # Skip this option if the crucial question doesn't match
        
        # Iterate over the numerical questions
        for i in range(1, 6):
            user_answer = getattr(user_data, f'answer{i}')
            expected_answer = numerical_values[i-1]
            if user_answer == expected_answer:
                score += 5  # Full points for an exact match
                specific_value = numerical_question_values.get(i, f"Question {i}")
                matching_details.append(f"{specific_value}")

        # Iterate over the non-crucial string-type questions
        for i in range(2, 6):
            user_answer = getattr(user_data, f'string_answer{i}')
            expected_answer = option_data.string_values[option][i-1]
            if user_answer == expected_answer:
                score += 5  # Adjust score for non-crucial string questions
                specific_value = string_question_values.get(i, f"String Question {i}")
                matching_details.append(f"{specific_value} ")

        # Check if stock is available
        if option_data.stock_data[option] > 0:
            option_scores[option] = score
            option_matching_details[option] = matching_details
    
    sorted_options = sorted(option_scores.items(), key=lambda x: x[1], reverse=True)
    
    return sorted_options, option_matching_details   

    #best_option = max(option_scores, key=option_scores.get) if option_scores else None
    #best_option_details = option_matching_details.get(best_option, [])
    
    #return best_option, option_scores, best_option_details      

    # Determine the best option
    if option_scores:
        best_option = max(option_scores, key=option_scores.get)
        best_option_info = option_data.preview_image_urls[best_option]
        

        print(f"Cevaplarınla en uyuşan koçumuz: {best_option}")
        print(f"Uyuşma puanınız: {option_scores[best_option]}")
        print(f"Uyuştuğunuz noktalar:")

        for detail in option_matching_details[best_option]:
            print(detail)  # Print each matching detail on a new line
        print(f"Koçumuza ulaşmak için: {best_option_info}")
        #print(f"Best Option: {best_option}, Score: {option_scores[best_option]}, Matched Questions: {matching_qs}, Info: {best_option_info}")
    else:
        print("No suitable option found based on the answers.")

# Rest of your existing code remains the same...


# Usage in Flask app
@app.route('/choose', methods=['POST'])
def choose():
    user_data = UserData()
    user_data.update_from_form(request.form)

    option_data = OptionData()


    #print("Received form data:", request.form)  # Debugging print
    #print("Updated user data:", vars(user_data))  # Debugging print
    
    sorted_options, option_matching_details = calculate_best_option(user_data, option_data)



    current_index = int(request.form.get('current_index', 0))  # Get the current index from the form


    print("Sorted options:", sorted_options)  # Debugging print


    print(len(sorted_options))
    if current_index < len(sorted_options):
        best_option = sorted_options[current_index][0]
        next_index = current_index + 1  # Prepare the next index for the next button click

        # Render a template with the results and the next index
        return render_template('results.html', 
                            user_data=user_data,  # add this line
                            best_option=best_option, 
                            user_name = user_data.name,
                            score=sorted_options[current_index][1],
                            matching_details=option_matching_details.get(best_option, []), 
                            option_info=option_data.urls.get(best_option, '#'),
                            picture_url=option_data.preview_image_urls.get(best_option, '#'),
                            current_index=current_index,
                            more_options_available=current_index < len(sorted_options))
    else:
        return redirect("https://shop.kantakademi.com/collections/koclarimiz")

if __name__ == '__main__':
    app.run(debug=True)


"""
    adjusted_scores = {
        name: option_data.scores[name] - abs(user_data.extra_number - option_data.inherent_numbers.get(name, 0))
                                        - abs(user_data.extra_number2 - option_data.inherent_numbers2.get(name, 0))
        for name in option_data.scores
    }

    options = {
        name: {
            'score': adjusted_scores[name],
            'url': option_data.urls[name],
            'stock': option_data.stock_data[name],
            'option_value': option_data.option_values[name],
            'preview_url': option_data.preview_image_urls[name]
        }
        for name in adjusted_scores
    }

    in_stock_options = {
        name: info for name, info in options.items()
        if info['stock'] > 0 and info['option_value'] == user_data.option_choice
    }

    sorted_options = sorted(in_stock_options.items(), key=lambda x: abs(x[1]['score'] - user_data.total_score))
    best_options = sorted_options[:2]

    print(f"Results for {user_data.name}:")
    for option_name, option_info in best_options:
        print(f"Option: {option_name}, Score: {option_info['score']}, URL: {option_info['url']}")

    return "Check the console for output."





"""

"""

def choose_best_option():

    # Hardcoded test data
    name = "Test User"
    total_score = 25  # Example total score
    option_choice = 'A'  # Example option choice
    extra_number = 7  # Example extra number
    extra_number2 = 5  # Example second extra number


    # Separate dictionaries for each attribute
    scores = {'Gül': 100, 'Eleya': 100, 'Rüya': 100}
    urls = {
        'Gül': 'https://shop.kantakademi.com/products/gul-rana',
        'Eleya': 'https://shop.kantakademi.com/products/eleya-ovul',
        'Rüya': 'https://shop.kantakademi.com/products/ruya'
    }
    stock_data = {'Gül': 2, 'Eleya': 2, 'Rüya': 2}
    option_values = {'Gül': 'A', 'Eleya': 'A', 'Rüya': 'A'}
    preview_image_urls = {
        'Gül': 'https://shop.kantakademi.com/cdn/shop/products/1EeoN_LzlHrnOd2LnUq9Ujt3kvnGtxvw5.jpg?v=1700439401&width=600',
        'Eleya': 'https://shop.kantakademi.com/cdn/shop/files/EleyaOvulMadak.jpg?v=1698185012&width=600',
        'Rüya': 'https://shop.kantakademi.com/cdn/shop/products/12yFqoDWkeVOHXwDCk3PJZ3sJ5SzaENVi.jpg?v=1700439387&width=360'
    }

    # Define a dictionary for the inherent number associated with each option
    inherent_numbers = {'Gül': 1, 'Eleya': 5, 'Rüya': 3}

    # Define a dictionary for the inherent number associated with each option
    inherent_numbers2 = {'Gül': 0, 'Eleya': 0, 'Rüya': 0}

    # Adjust the scores based on the extra number provided by the user
    adjusted_scores = {
        name: scores[name] - abs(extra_number - inherent_numbers.get(name, 0))
                            -abs(extra_number2 - inherent_numbers2.get(name, 0))
        for name in scores
    }

    # Combine attributes for each option
    options = {
        name: {
            'score': adjusted_scores[name],
            'url': urls[name],
            'stock': stock_data[name],
            'option_value': option_values[name],
            'preview_url': preview_image_urls[name]
        }
        for name in adjusted_scores
    }

    # Filter options based on selection and stock
    in_stock_options = {
        name: info for name, info in options.items()
        if info['stock'] > 0 and info['option_value'] == option_choice
    }



    # Sort and select the best options
    sorted_options = sorted(in_stock_options.items(), key=lambda x: abs(x[1]['score'] - total_score))
    best_options = sorted_options[:2]

    # Print results to the console
    print(f"Results for {name}:")
    for option_name, option_info in best_options:
        print(f"Option: {option_name}, Score: {option_info['score']}, URL: {option_info['url']}")

    return "Check the console for output."


choose_best_option()
"""
#if __name__ == '__main__':
 #   app.run(debug=True, host='0.0.0.0')



"""
    # Generate HTML content for the best options
    best_options_content = ""
    for option_name, option_info in best_options:
        best_options_content += f'''
            <div class="result">
                <h2>{option_name}</h2>
                <img src="{option_info['preview_url']}" alt="Önizleme" class="option-image">
                <div class="button-container">
                    <a href="{option_info['url']}" target="_blank">
                        <button style="background-color: #b60000; color: white;">Koçluğa Başla!</button>
                    </a>
                </div>
            </div>
        '''

    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sonuç Sayfası</title>
        <style>
            body {{ text-align: center; }}
            .results-container {{
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
            }}
            .result {{
                margin: 10px;
                flex-basis: calc(50% - 20px);
                text-align: center;
                box-sizing: border-box;
            }}
            .option-image {{
                width: 100%;
                max-width: 250px;
                height: auto;
                margin: auto;
                display: block;
            }}
            .button-container {{ margin-top: 10px; }}
            .button-container button {{
                background-color: #b60000;
                color: white;
                padding: 10px 20px;
                border: none;
                cursor: pointer;
            }}
        </style>
    </head>
    <body>
        <h1>{name}, senin için en uygun iki seçenek:</h1>
        <div class="results-container">
            {best_options_content}
        </div>
    </body>
    </html>
    '''
"""



