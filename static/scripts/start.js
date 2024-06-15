$(document).ready(function () {
  // Tries to force the video to be rendered and autoplayed on ios devices

  if (!sessionStorage.getItem("route_id")) {
    sessionStorage.setItem("route_id", "0");
  }
  console.log(sessionStorage.getItem("route_id"));

  let route = parseInt(sessionStorage.getItem("route_id"));
  console.log(route);

  if (route === 0) {
    $(".button_prev").hide();
    // console.log(route)
  } else {
    $(".button_prev").show();
  }

  if (route < 9) {
    $(".button_submit").hide();
  }

  if (route > 8) {
    $(".button_next").hide();
    $(".button_submit").show();
    // console.log(route)
  }

  // Increment route ID and navigate to next route
  $(".button_next").click(function () {
    route++;

    sessionStorage.setItem("route_id", route.toString());
    window.location.href = "/play_now/" + route;
  });

  // Decrement route ID and navigate to previous route
  $(".button_prev").click(function () {
    route--;

    // Use Callbacks or Promises
    // Ensuring that navigation to the next route
    // only occurs aftern sessionStorage operation has completed
    sessionStorage.setItem("route_id", route.toString());
    window.location.href = "/play_now/" + route;
  });

  // Play_now button
  // Navigate to the initial route when clicking the start random button
  $(".button_start-random").click(function () {
    console.log("working");
    sessionStorage.clear();

    sessionStorage.setItem("difficulty", "any");
    sessionStorage.setItem("category", "any");

    if (sessionStorage.getItem("route_id")) {
      sessionStorage.setItem("route_id", "0");
    }
    window.location.href = "/play_now";
    console.log("not_Working");
  });

  // const difficulty = $("#trivia-difficulty").val();
  // console.log(difficulty);
  // console.log($("#trivia-difficulty").val());
  // console.log("BUHAHAHAHAHHAHAA");

  $(".button_trivia-start").on("click", function () {
    sessionStorage.clear();

    // console.log("Testingg");
    // console.log("Testingg");

    const difficulty = $("#trivia-difficulty").val();
    const category = $("#trivia-category").val();
    console.log(difficulty, category);
    // console.log("Testingg");

    sessionStorage.setItem("difficulty", difficulty);
    sessionStorage.setItem("category", category);
  });

  const isCompletedAnswers = [
    "radioSelection0",
    "radioSelection1",
    "radioSelection2",
    "radioSelection3",
    "radioSelection4",
    "radioSelection5",
    "radioSelection6",
    "radioSelection7",
    "radioSelection8",
    "radioSelection9",
  ];

  // Function to check if all answers are completed
  // only return true if all isCompletedAnswers is not null
  function checkCompletedAnswers() {
    return isCompletedAnswers.every(function (question) {
      // console.log(sessionStorage.getItem(question));
      return sessionStorage.getItem(question) !== null;
    });
  }

  // restores the slected input for each page if a selectin
  // has previously been made
  function restoreSelectedAnswer() {
    const selectedAnswer = sessionStorage.getItem("radioSelection" + route);
    if (selectedAnswer !== null) {
      $('input[name="selected_answer"][value="' + selectedAnswer + '"]').prop(
        "checked",
        true
      );
    }
  }
  restoreSelectedAnswer();

  // Initially disable the submit button
  $(".button_submit").prop("disabled", true);

  // Enable submit button if all answers are completed and on the final route
  if (checkCompletedAnswers() && route === 9) {
    $(".button_submit").prop("disabled", false);
  }

  // console.log($("selcted_answer-radio"));
  $(".container_answer").on("click", function () {
    // $("selcted_answer-radio").prop("checked", true);
    $(this).find("input[type='radio']").prop("checked", true).trigger("change");
  });

  // $(".container_answer").on("click", function () {
  //   // for (let i = 0; i < 4; i++) {
  //   //   $('input[id="selected_answer-' + i + '"]')
  //   //     .prop("checked", true)
  //   //     .trigger("click");
  //   // }
  //   $(this).find('input[type="radio"]').prop("checked", true).trigger("click");
  // });

  // Event handler for radio button click
  $('input[name="selected_answer"]').on("change", function () {
    const selectedAnswer = $('input[name="selected_answer"]:checked').val();
    sessionStorage.setItem("radioSelection" + route, selectedAnswer);
    // restoreSelectedAnswer(); //reload selections upon click

    if (checkCompletedAnswers() && route === 9) {
      console.log("completed" + checkCompletedAnswers());
      $(".button_submit").prop("disabled", false);
    } else {
      // siabled = $(".button_submit").prop("disabled", true);
      console.log("completed" + checkCompletedAnswers());
    }
  });

  // Trivia Submit button
  // Collects all the input, stores them in an object
  // stringify them and send along with the form to the app server
  $(".button_submit").on("click", function () {
    console.log("HELOOOOOOOOOOOOO");

    const selectedAnswersList = {};
    for (let i = 0; i < 10; i++) {
      selectedAnswersList["answer" + i] = sessionStorage.getItem(
        "radioSelection" + i
      );
    }

    // Convert selectedAnswersList object to JSON string
    // before sending it over the network
    const selectedAnswersJson = JSON.stringify(selectedAnswersList);

    $("<input>")
      .attr({
        type: "hidden",
        name: "selected_answers",
        value: selectedAnswersJson,
      })
      .appendTo('form[action="/score"]');
  });

  // $(".button_home").on("click", function () {
  //   window.location.href = "/";
  // });
  $(".button_results-view").on("click", function () {
    window.location.href = "/results";
  });

  // ajax to send post request when restarti clicked
  // gets users current settings/preferences and uses
  // it to start a new game.
  $(".button_restart").on("click", function () {
    // console.log("WORKING FOR HERE");
    $.ajax({
      type: "POST",
      url: "/submit_mode",
      data: {
        trivia_difficulty: sessionStorage.getItem("difficulty"),
        trivia_category: sessionStorage.getItem("category"),
      },
      success: function (response) {
        // Handle success (e.g., redirect, show a message, etc.)
        console.log("request sent successfully", response);
        sessionStorage.clear();
        window.location.href = response.redirect_url;
      },
      error: function (error) {
        // Handle error
        console.error("Error", error);
      },
    });
  });

  // FOR RESULTS PAGE
  // const correctAnswersList = JSON.parse($("#answers_data").data("correct-answers"));
  // let correctAnswersList = $("#answers_data").data("correct-answers");
  // console.log($("#answers_data").text());
  let correctAnswersList = JSON.parse($("#answers_data").text());
  console.log(correctAnswersList);
  console.log(typeof correctAnswersList);

  for (let i = 0; i < 10; i++) {
    // answer1 = $(".question_" + i + "#answer_1").val();
    // answer2 = $(".question_" + i + "#answer_2").val();
    // answer3 = $(".question_" + i + "#answer_3").val();
    // answer4 = $(".question_" + i + "#answer_4").val();
    // answer_list = [answer1, answer2, answer3, answer4];

    // Adds a new class green if the selected answer is correct
    // The class is used to style the correct answer
    const correctAnswer = correctAnswersList[i];
    console.log("correctanswer", correctAnswer);
    const answerSelected = sessionStorage.getItem("radioSelection" + i);
    console.log("answerselected", answerSelected);
    if (answerSelected === correctAnswer) {
      $(".question_" + i).each(function () {
        if ($(this).text().trim() === correctAnswer) {
          console.log("truthy");
          $(this).addClass("green-box");
        }
      });
    }

    // Adds a new class red if the selected answer is wrong
    // The class is used to style the wrong answer
    if (answerSelected !== correctAnswer) {
      $(".question_" + i).each(function () {
        if ($(this).text().trim() === answerSelected) {
          console.log("falsey", $(this).text(), answerSelected);
          $(this).addClass("red-box");
        }
        if ($(this).text().trim() === correctAnswer) {
          console.log("falsey", $(this).text(), answerSelected);
          $(this).addClass("green-box");
        }
      });
    }
  }

  const guruHomeVideo = $("#guru-home-video")[0];
  guruHomeVideo.autoplay = true;
  guruHomeVideo.load();
});
