// Define the base api url
var base_url = 'https://655735yxlatbe5ywa5hbmdutpi0bjxlt.lambda-url.us-east-1.on.aws';


// Get the collector humidity data from the API
async function getCollectorHumidity(collector_id, limit = 100) {
  const response = await fetch(`${base_url}/collector/${collector_id}/calculated_humidity?limit=${limit}`);
  const data = await response.json();
  return {
    labels: data.data.map(record => new Date(record.calculation_date).toLocaleDateString('pt-BR', { month:"numeric", day:"numeric", hour:"numeric", minute:"numeric", seconds:"numeric"})),
    data: data.data.map(record => record.humidity_percentage),
  }
}

// Setups the chart
const ctx = document.getElementById('myChart');
var myChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: [],
    datasets: [{
      label: '1',
      data: [],
    }]
  },
  options: {
    maintainAspectRatio: false,
    scales: {
      x: {
        title: {
          text: 'Data de leitura',
          display: true,
        }
      },
      y: {
        ticks: {
          callback: (label) => `${label}%`
        },
        title: {
          text: 'Umidade',
          display: true,
        },
      }
    },
    plugins: {
      title: {
        text: 'Umidade do solo',
        font: {
          size: 20,
        },
        display: true,
      },
      legend: {
        title: {
          text: 'Coletor',
          display: true,
        },
        display: true,
      }
    }
  }
});

// Initialize the chart
async function createChart(collector_id) {
  const data = await getCollectorHumidity(collector_id);
  // revert the order of the data
  myChart.data.labels = data.labels.reverse();
  myChart.data.datasets[0].data = data.data.reverse();
  myChart.update();
}

// Update the chart
async function updateChart(collector_id) {
  const data = await getCollectorHumidity(collector_id, limit = 1);
  // if last label is the same as the new one, skip the update
  if (myChart.data.labels[myChart.data.labels.length - 1] === data.labels[0]) return;
  myChart.data.labels.push(data.labels[0]);
  myChart.data.labels.shift();
  myChart.data.datasets[0].data.push(data.data[0]);
  myChart.data.datasets[0].data.shift();
  myChart.update();
}

// Create the chart and update it every 10 seconds
createChart(1);
setInterval(() => {updateChart(1)}, 10000);
