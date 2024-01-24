document.addEventListener("DOMContentLoaded", function() {
  let id = (id) => document.getElementById(id);
  let form = id("titanic-form"); // Ensure your form has the id="titanic-form"

  form.addEventListener("submit", (e) => {
      e.preventDefault();

      // Collect data from the form
      let formData = {
          Pclass: ['1st', '2nd', '3rd'].indexOf(id("pclass").value.trim()) + 1,
          Sex: id("sex").value.trim() == "male" ? 1 : 0,
          Age: Number(id("age").value.trim()),
          SibSp: Number(id("sibsp").value.trim()),
          Parch: Number(id("parch").value.trim()),
          Fare: Number(id("fare").value.trim()),
          Embarked: ['C', 'Q', 'S'].indexOf(id("embarked").value.trim()),
      };

      // Validate and send request
      if (validateForm(formData)) {
          sendPredictionRequest(formData);
      }
  });

  // Function to validate form data
  function validateForm(data) {
      let isValid = true;
      // for (const [key, value] of Object.entries(data)) {
      //     if (value === "" || isNaN(value)) {
      //         displayError(key, `${key.replace(/_/g, " ")} cannot be blank or non-numeric where applicable`);
      //         isValid = false;
      //     } else {
      //         clearError(key);
      //     }
      // }
      return isValid;
  }

  // Function to display error
  function displayError(fieldId, message) {
      let field = id(fieldId);
      let errorDiv = field.nextElementSibling; // Make sure there is a div to display the error after each input
      errorDiv.innerHTML = message;
      field.style.border = "2px solid red";
  }

  // Function to clear error
  function clearError(fieldId) {
      let field = id(fieldId);
      let errorDiv = field.nextElementSibling; // Make sure there is a div to display the error after each input
      errorDiv.innerHTML = "";
      field.style.border = "";
  }

  // Function to send POST request to the server
  function sendPredictionRequest(data) {
      fetch(`${window.location.origin}/predict/logistic_regression`, { // Adjust the endpoint as needed
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify(data)
      })
      .then(response => response.json())
      .then(data => {
          console.log('Success:', data);
          alert(`Survived?: ${data.survived}`);
      })
      .catch((error) => {
          console.error('Error:', error);
          alert('An error occurred while making the prediction');
      });
  }
});
