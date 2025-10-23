document.addEventListener("DOMContentLoaded", () => {
  const stateSelect = document.getElementById("stateSelect");
  const lgaSelect = document.getElementById("lgaSelect");

  // fetch states_lgas.json
  fetch("/static/data/states_lgas.json")
    .then(res => res.json())
    .then(statesLgas => {

      function populateLgas(state){
        lgaSelect.innerHTML = "";
        if(!statesLgas[state]){
          lgaSelect.innerHTML = '<option value="">Select state first</option>';
          return;
        }
        statesLgas[state].forEach(lga => {
          const opt = document.createElement("option");
          opt.value = lga;
          opt.text = lga;
          lgaSelect.appendChild(opt);
        });
      }

      stateSelect.addEventListener("change", e => populateLgas(e.target.value));

      // initial populate if a state is pre-selected
      if(stateSelect.value) populateLgas(stateSelect.value);
    });
});
