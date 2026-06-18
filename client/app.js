function getBathValue() {
  var uiBathrooms = document.getElementsByName("uiBathrooms");
  for(var i = 0; i < uiBathrooms.length; i++) {
    if(uiBathrooms[i].checked) {
        return parseInt(uiBathrooms[i].value);
    }
  }
  return -1; // Invalid Value
}

function getBHKValue() {
  var uiBHK = document.getElementsByName("uiBHK");
  for(var i = 0; i < uiBHK.length; i++) {
    if(uiBHK[i].checked) {
        return parseInt(uiBHK[i].value);
    }
  }
  return -1; // Invalid Value
}

function onClickedEstimatePrice() {
  console.log("Estimate price button clicked");
  var sqft = document.getElementById("uiSqft");
  var bhk = getBHKValue();
  var bathrooms = getBathValue();
  var location = document.getElementById("uiLocations");
  var estPrice = document.getElementById("uiEstimatedPrice");
  var submitBtn = document.querySelector(".submit");

  if(bhk === -1 || bathrooms === -1) {
    estPrice.innerHTML = "<h2 style='color: #FF6B6B;'>Please select BHK and Bathrooms</h2>";
    return;
  }

  if(!location.value) {
    estPrice.innerHTML = "<h2 style='color: #FF6B6B;'>Please select a location</h2>";
    return;
  }

  // Show loading state
  submitBtn.disabled = true;
  submitBtn.textContent = "Estimating...";
  submitBtn.style.opacity = "0.7";
  estPrice.innerHTML = "<h2 style='color: #94A3B8;'>Calculating price...</h2>";

  var url = getApiUrl("/predict_home_price");

  $.post(url, {
      total_sqft: parseFloat(sqft.value),
      bhk: bhk,
      bath: bathrooms,
      location: location.value
  }, function(data, status) {
      console.log("Price estimated:", data.estimated_price);
      estPrice.innerHTML = "<h2>₹" + data.estimated_price.toString() + " Lakh</h2>";
      console.log("Status:", status);
  }).fail(function(error) {
      console.error("Error:", error);
      estPrice.innerHTML = "<h2 style='color: #FF6B6B;'>Error: Could not connect to server. Is Flask running?</h2>";
  }).always(function() {
      // Reset button state
      submitBtn.disabled = false;
      submitBtn.textContent = "Estimate Price";
      submitBtn.style.opacity = "1";
  });
}

function onPageLoad() {
  console.log("document loaded");
  var url = getApiUrl("/get_location_names");
  $.get(url, function(data, status) {
      console.log("got response for get_location_names request");
      if(data && data.locations) {
          var locations = data.locations;
          var uiLocations = document.getElementById("uiLocations");
          $('#uiLocations').empty();
          $('#uiLocations').append(new Option("Choose a Location", ""));
          for(var i = 0; i < locations.length; i++) {
              var opt = new Option(locations[i]);
              $('#uiLocations').append(opt);
          }
      }
  }).fail(function(error) {
      console.error("Error loading locations:", error);
      var estPrice = document.getElementById("uiEstimatedPrice");
      estPrice.innerHTML = "<h2 style='color: #FF6B6B;'>Error: Server not running at " + getApiUrl("") + "</h2>";
  });
}

window.onload = onPageLoad;