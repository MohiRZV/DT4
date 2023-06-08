$(document).ready(function() {
    $('#uploadForm').submit(function(event) {
        event.preventDefault();
        var formData = new FormData(this);

        $.ajax({
          url: '/upload',
          type: 'POST',
          data: formData,
          processData: false,
          contentType: false,
          success: function(response) {
            alert(response); // Show a success message
          },
          error: function(xhr, status, error) {
            alert('Error: ' + error); // Show an error message
          }
        });
        $("#prediction-result").text("");
        $("#display-area-ml").text("");
    });
    // Button click event handlers
    $("#button1").click(function() {
        scrollToTop()
        displayShape();
    });

    $("#button2").click(function() {
        scrollToTop()
        displayDtypes();
    });

    $("#button3").click(function() {
        scrollToTop()
        addNumericInput(displayHead)
    });

    $("#button4").click(function() {
        scrollToTop()
        addNumericInput(displayTail)
    });

    $("#button5").click(function() {
        scrollToTop()
        displayStatistics();
    });

    $("#button6").click(function() {
        scrollToTop()
        displayDropna()
    });

    $("#buttonFeatures").click(function() {
        displayFeatures();
    });

    $("#buttonOneHot").click(function() {
        oneHotEncode();
    });

    $("#buttonLabelEncode").click(function() {
        labelEncode();
    });

    $("#buttonTrain").click(function() {
        train();
    });


  $("#button-predict").on("click", function(event) {
    event.preventDefault();

    var formData = $("#fieldsForm").serialize();

    $.ajax({
      type: "POST",
      url: "/diamonds",
      data: formData,
      success: function(response) {
        $("#prediction-result").text(response);
      },
      error: function(error) {
        console.log(error);
      }
    });
    $("#prediction-result").text("Processing");
  });

  $(document).on("submit", "#columnForm", function(event) {
    event.preventDefault();

    var formData = $("#columnForm").serialize();

    $.ajax({
      type: "POST",
      url: "/select_features",
      data: formData,
      success: function(response) {
        $("#selected_columns").text(response);
      },
      error: function(error) {
        console.log(error);
      }
    });
  });

  $(document).on("submit", "#predictForm", function(event) {
    event.preventDefault();

    var formData = $("#predictForm").serialize();

    $.ajax({
      type: "POST",
      url: "/predict",
      data: formData,
      success: function(response) {
        $("#result").text(response);
      },
      error: function(error) {
        alert("Invalid inputs or model not trained!");
        console.log(error);
      }
    });
  });

  function addNumericInput(submitFunction) {
    // Get the container element
    var container = document.getElementById('display-area');
    container.innerHTML = "";
    // Create the numeric input field
    var inputField = document.createElement('input');
    inputField.type = 'number';
    $("#result-title").text("How many?");
    // Create the submit button
    var submitButton = document.createElement('button');
    submitButton.textContent = 'Submit';

    // Add an event listener to the submit button
    submitButton.addEventListener('click', function() {
        var inputValue = inputField.value; // Get the value from the input field

        // Handle the submission of the numeric input value
        // You can perform further processing or validation here
        console.log('Submitted value:', inputValue);
        submitFunction(inputValue);
    });
    // Append the input field and submit button to the container
    container.appendChild(inputField);
    container.appendChild(submitButton);
  }

  function scrollToTop() {
    // Get the table wrapper element
    var tableWrapper = document.querySelector('.custom-table-wrapper');

    // Reset the scrollbar to the top
    tableWrapper.scrollTop = 0;
  }

  // Function to display Table 1
  function displayShape() {
    // Make an AJAX request to the server to fetch the table data
    $.ajax({
      url: "/shape",
      method: "GET",
      success: function(response) {
        $("#display-area").html(response);
        $("#result-title").text("Shape");
      },
      error: function(error) {
        console.log(error);
      }
    });
  }

  // Function to display Table 2
  function displayDtypes() {
    // Make an AJAX request to the server to fetch the table data
    $.ajax({
      url: "/dtypes",
      method: "GET",
      success: function(response) {
        $("#display-area").html(response);
        $("#result-title").text("Dtypes");
      },
      error: function(error) {
        console.log(error);
      }
    });
  }

  // Function to display a result
  function displayHead(inputValue) {
    // Make an AJAX request to the server to fetch the result
    $.ajax({
      url: "/head?n="+inputValue,
      method: "GET",
      success: function(response) {
        $("#display-area").html("");
        $("#display-area").html(response);
        $("#result-title").text("Head");
      },
      error: function(error) {
        console.log(error);
      }
    });
  }

  // Function to display a result
  function displayTail(inputValue) {
    // Make an AJAX request to the server to fetch the result
    $.ajax({
      url: "/tail?n="+inputValue,
      method: "GET",
      success: function(response) {
        $("#display-area").html(response);
        $("#result-title").text("Tail");
      },
      error: function(error) {
        console.log(error);
      }
    });
  }

  // Function to display a result
  function displayStatistics() {
    // Make an AJAX request to the server to fetch the result
    $.ajax({
      url: "/statistics",
      method: "GET",
      success: function(response) {
        $("#display-area").html(response);
        $("#result-title").text("Statistics");
      },
      error: function(error) {
        console.log(error);
      }
    });
  }
  function displayDropna() {
    // Make an AJAX request to the server to fetch the table data
    $.ajax({
      url: "/dropna",
      method: "GET",
      success: function(response) {
        $("#display-area").html(response);
        $("#result-title").text("Dropna");
      },
      error: function(error) {
        console.log(error);
      }
    });
  }

  function displayFeatures() {
    $.ajax({
      url: '/get_features',
      type: 'GET',
      success: function(response) {
        // Load the form content into the container div
        $('#formContainer').html(response);
      },
      error: function(error) {
        console.log(error);
      }
    });
  }

  function oneHotEncode() {
    $.ajax({
      url: '/one_hot_encode',
      type: 'GET',
      success: function(response) {
        // Load the form content into the container div
        $('#display-area-ml').html(response);
      },
      error: function(error) {
        alert("No features selected!");
        console.log(error);
      }
    });
  }

  function labelEncode() {
    $.ajax({
      url: '/label_encode',
      type: 'GET',
      success: function(response) {
        // Load the form content into the container div
        $('#display-area-ml').html(response);
      },
      error: function(error) {
        alert("No features selected!");
        console.log(error);
      }
    });
  }

  function train() {
    var algorithm = $("#algorithm").val();
    $('#display-area-ml').html("Training " + algorithm);

    $.ajax({
      type: "POST",
      url: "/train",
      data: {algorithm: algorithm},
      success: function(response) {
        alert("Model finished training!");
        $('#testContainer').html(response)
      },
      error: function(error) {
        console.log(error);
      }
    });
  }

});
