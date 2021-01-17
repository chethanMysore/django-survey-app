/***
Custom JS file to make AJAX calls using JQuery and populating survey statics and rendering visualizations

Here we make REST calls to get the popular_survey and nested survey objects using AJAX and JQuery.
document.ready:
---------------
document.ready is the entry point for the script and will be called
once the DOM loads HTMl elements on the browser canvas.


***/
$(document).ready(function(){

  // Local Variables
  let popular_survey = null
  let popular_survey_name = ""
  let popular_survey_id = null
  let surveys = []
  let questions = []
  let selected_questions = []
  let choices = []
  let selected_survey_id = null
  let selected_question_id = null

  // REST GET call to fetch all surveys which returns a stringified JSON
  // with object lists for each of the entities.
  $.ajax({url: "http://localhost:8000/survey/get_all_surveys/", success: function(result){
      if(!!result){
        try{
            if(!!result.surveys){

                // Parse JSON string to object and populate surveys array
                let surveys_json = JSON.parse(result.surveys)
                if(Array.isArray(surveys_json)){
                    surveys_json.forEach((survey, index) => {
                        surveys.push({surveyId: survey.pk, surveyName: survey.fields.name})
                    })

                    // Create Survey dropdown options
                    $.each(surveys, function(index, survey) {
                        $('#surveys-dropdown')
                             .append($("<option></option>")
                             .attr("value", survey.surveyId)
                             .text(survey.surveyName));
                    });
                }

                // Parse JSON string to object and populate questions array
                let questions_json = JSON.parse(result.questions)
                if(Array.isArray(questions_json)){
                    questions_json.forEach((question, index) => {
                        questions.push({questionId: question.pk, questionText: question.fields.question_text,
                        surveyId: question.fields.survey})
                    })
                }

                // Parse JSON string to object and populate choices array
                let choices_json = JSON.parse(result.choices)
                if(Array.isArray(choices_json)){
                    choices_json.forEach((choice, index) => {
                        choices.push({questionId: choice.fields.question, choiceText: choice.fields.choice_text,
                        choiceId: choice.pk, votes: choice.fields.votes})
                    })
                }
            }
        }
        catch(err){
            console.log("err occurred while parsing result response: ", err)
        }
      }
  }});

  // REST GET call to retrieve the popular survey object based number of survey submissions.
  $.ajax({url: "http://localhost:8000/survey/get_popular_survey/", success: function(result){
      if(!!result){
        try{
            popular_survey = JSON.parse(result)
            if(Array.isArray(popular_survey)){
                popular_survey = popular_survey[0]
                popular_survey_id = popular_survey.pk
                popular_survey_name = popular_survey.fields.name

                // Update the table cell value with the link to popular survey item
                $("#popular-survey").text(popular_survey_name)
                $("#popular-survey").attr("href", `http://localhost:8000/admin/survey/survey/${popular_survey_id}`)
            }
        }
        catch(err){
            console.log("err occurred while parsing result response: ", err)
        }
      }
  }});

  // On selecting a survey, create respective questions options for questions dropdown
  $("#surveys-dropdown").click(function(){
    selected_survey_id = $("#surveys-dropdown option:selected").val()
    if(Array.isArray(surveys)){
        selected_questions = questions.filter(question => question.surveyId == selected_survey_id)
    }

    // Make sure to reset the drop down list to ensure removal of questions from another survey
    $('#questions-dropdown')
    .find('option')
    .remove()
    .end()
    .append('<option value="Select a Question">Select a Question</option>')
    .val('Select a Question')

    // Create dropdown options for the questions dropdown
    $.each(selected_questions, function(index, question) {
        $('#questions-dropdown')
            .append($("<option></option>")
            .attr("value", question.questionId)
            .text(question.questionText));
    });
  })

  // On selecting a question, filter the choices for the question and
  // render the chart with the vote statistics for the question
  $("#questions-dropdown").click(function(){
    selected_question_id = $("#questions-dropdown option:selected").val()
    if(Array.isArray(questions)){
        selected_choices = choices.filter(choice => choice.questionId == selected_question_id)
    }
    renderChart(selected_choices)
  })

  // Helper to create chart.js bar chart with the choices for selected question
  const renderChart = (selected_choices) => {
    selected_choices = !!selected_choices && Array.isArray(selected_choices) ? selected_choices : []
    let ctx = document.getElementById('votes_bar_chart')
    if(!!ctx){
        ctx = ctx.getContext('2d');
        let votes_bar_chart = new Chart(ctx, {
            type: 'bar',
            data: {

                // Returns list of choice texts for X-axis
                labels: selected_choices.map(choice => choice.choiceText),
                datasets: [{
                    label: '# of Votes',
                    // Returns list of votes for Y-axis
                    data: selected_choices.map(choice => choice.votes),
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        });
    }
  }

  renderChart()

});