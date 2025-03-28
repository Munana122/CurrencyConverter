document.addEventListener("DOMContentLoaded", () => {
  const fromCurrency = document.getElementById("fromCurrency");
  const toCurrency = document.getElementById("toCurrency");


  const API_URL = ""; // Flask backend address left blank to take the current address

  // Populate dropdowns dynamically from the backend
  async function fetchCurrencies() {
      try {
          const response = await fetch(`${API_URL}/currencies`);
          const data = await response.json();

          if (data.error) {
              console.error("Error fetching currencies:", data.error);
              return;
          }

          data.currencies.forEach(currency => {
              const option1 = new Option(currency, currency);
              const option2 = new Option(currency, currency);
              fromCurrency.add(option1);
              toCurrency.add(option2);
          });

          
          fromCurrency.value = "USD";
          toCurrency.value = "EUR";
      } catch (error) {
          console.error("Failed to fetch currencies:", error);
      }
  }

  fetchCurrencies();
});

// Make convertCurrency globally accessible
async function convertCurrency() {
  const fromCurrency = document.getElementById("fromCurrency").value;
  const toCurrency = document.getElementById("toCurrency").value;
  const amount = document.getElementById("amount").value;
  const resultDiv = document.getElementById("result");

  if (!amount || amount <= 0) {
      resultDiv.textContent = "Please enter a valid amount.";
      return;
  }

  try {
      const API_URL = "";
      const response = await fetch(`${API_URL}/convert?from=${fromCurrency}&to=${toCurrency}&amount=${amount}`);
      const data = await response.json();

      if (data.error) {
          resultDiv.textContent = `Error: ${data.error}`;
      } else {
          resultDiv.textContent = `${amount} ${fromCurrency} = ${data.converted_amount} ${toCurrency}`;
      }
  } catch (error) {
      console.error("Error fetching exchange rate:", error);
      resultDiv.textContent = "Conversion failed. Try again.";
  }
}
