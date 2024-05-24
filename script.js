const CURRENCIES = ["AUD", "EUR", "USD", "CAD", "GBP", "JPY", "CNY", "INR", "KRW"];


window.addEventListener('load', () => {
    const currencySelect = document.getElementById('baseCurrency');

    CURRENCIES.forEach(currency => {
        const option = document.createElement('option');
        option.value = currency;
        option.textContent = currency;
        currencySelect.appendChild(option);
    });
});
document.getElementById('convertBtn').addEventListener('click', async () => {
    const baseCurrency = document.getElementById('baseCurrency').value;
    const baseValue = document.getElementById('baseValue').value;
    const DECODED_TOKEN = atob('ZmNhX2xpdmVfbXlZMnhCRnQ2Mlk1TktETGVQeXNoaVJ0eHRaNm4wNm03YXdxWmM4bA==');
    const CURR_TOKEN = `${ DECODED_TOKEN }`;
    const CURRENCY_ICONS = {
        "USD": "<strong class='has-text-primary'>$</strong>",
        "EUR": "<strong class='has-text-primary'>€</strong>",
        "AUD": "<strong class='has-text-primary'>A$</strong>",
        "CAD": "<strong class='has-text-primary'>C$</strong>",
        "GBP": "<strong class='has-text-primary'>£</strong>",
        "JPY": "<strong class='has-text-primary'>¥</strong>",
        "CNY": "<strong class='has-text-primary'>¥</strong>",
        "INR": "<strong class='has-text-primary'>₹</strong>",
        "KRW": "<strong class='has-text-primary'>₩</strong>",
    }
    const response = await fetch(`https://api.freecurrencyapi.com/v1/latest?apikey=${CURR_TOKEN}&base_currency=${baseCurrency}&currencies=${CURRENCIES}`);
    const data = await response.json();

    const resultsDiv = document.getElementById('results');
    
    resultsDiv.innerHTML = '';

    if (data.error) {
        resultsDiv.innerHTML = `<p>${data.error}</p>`;
        return;
    }

    const table = document.createElement('table');
    table.classList.add('table', 'is-striped', 'is-hoverable', 'has-background-black-ter')
    const thead = document.createElement('thead');
    const tbody = document.createElement('tbody');

    const headerRow = document.createElement('tr');
    headerRow.innerHTML = `<th>Currency</th><th>Rate</th>`;
    thead.appendChild(headerRow);

    for (const [currency, rate] of Object.entries(data.data)) {
        if (currency === baseCurrency) {
            continue;
        }
        const row = document.createElement('tr');
        if (baseValue) {
            const convertedValue = baseValue * rate;
            row.innerHTML = `<td>${currency}</td><td>${CURRENCY_ICONS[currency]}${convertedValue.toFixed(2)}</td>`;
        }
        else {
            row.innerHTML = `<td>${currency}</td><td>${CURRENCY_ICONS[currency]}${rate.toFixed(2)}</td>`;
        }
        tbody.appendChild(row);
    }

    table.appendChild(thead);
    table.appendChild(tbody);
    resultsDiv.appendChild(table);
    // resultsDiv.classList.add('box','has-background-black-ter', 'theme-dark');
});