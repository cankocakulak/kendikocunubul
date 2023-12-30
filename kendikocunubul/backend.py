from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    # Render the HTML form
    return render_template('firstpage.html')  # Ensure 'form.html' is in the 'templates' directory.


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


