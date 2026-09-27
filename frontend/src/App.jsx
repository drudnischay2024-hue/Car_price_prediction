import React, { useState, useEffect } from 'react';
import { Activity, Car, DollarSign, Database, Tag } from 'lucide-react';

const API_BASE_URL = 'http://localhost:8000';

function App() {
  const [metrics, setMetrics] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Default values set to average/typical values from the dataset
  const [formData, setFormData] = useState({
    MPG_city: 25,
    MPG_highway: 30,
    EngineSize: 2.0,
    Horsepower: 140,
    RPM: 5500,
    Rev_per_mile: 2500,
    Fuel_tank_capacity: 15.0,
    Passengers: 5,
    Length: 180,
    Wheelbase: 100,
    Width: 68,
    Turn_circle: 38,
    Rear_seat_room: 27,
    Luggage_room: 14,
    Weight: 3000,
    Type: 'Small',
    AirBags: 'Driver only',
    DriveTrain: 'Front',
    Cylinders: '4',
    Man_trans_avail: 'Yes',
    Origin: 'non-USA'
  });

  useEffect(() => {
    fetch(`${API_BASE_URL}/metrics`)
      .then(res => res.json())
      .then(data => setMetrics(data))
      .catch(err => console.error("Error fetching metrics", err));
  }, []);

  const handleChange = (e) => {
    const { name, value, type } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'number' ? Number(value) : value
    });
  };

  const handlePredict = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setPrediction(null);
    try {
      const res = await fetch(`${API_BASE_URL}/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      if (!res.ok) throw new Error('Prediction failed');
      const data = await res.json();
      setPrediction(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 text-gray-800 font-sans p-4 md:p-8">
      <div className="max-w-6xl mx-auto space-y-8">
        
        {/* Header */}
        <header className="flex items-center space-x-3 pb-6 border-b border-gray-200">
          <div className="bg-blue-600 p-3 rounded-lg shadow-sm">
            <Car className="text-white w-8 h-8" />
          </div>
          <div>
            <h1 className="text-3xl font-bold text-gray-900 tracking-tight">Car Price Prediction System</h1>
            <p className="text-gray-500">Machine Learning Regression Project</p>
          </div>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Left Column: Form */}
          <div className="lg:col-span-2 bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
            <h2 className="text-xl font-semibold mb-6 flex items-center">
              <Tag className="w-5 h-5 mr-2 text-blue-500" />
              Enter Vehicle Specifications
            </h2>
            <form onSubmit={handlePredict} className="grid grid-cols-1 md:grid-cols-2 gap-5">
              
              <div className="space-y-1">
                <label className="text-sm font-medium text-gray-600">Car Type</label>
                <select name="Type" value={formData.Type} onChange={handleChange} className="w-full p-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition">
                  <option value="Small">Small</option>
                  <option value="Compact">Compact</option>
                  <option value="Midsize">Midsize</option>
                  <option value="Large">Large</option>
                  <option value="Sporty">Sporty</option>
                  <option value="Van">Van</option>
                </select>
              </div>

              <div className="space-y-1">
                <label className="text-sm font-medium text-gray-600">Origin</label>
                <select name="Origin" value={formData.Origin} onChange={handleChange} className="w-full p-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition">
                  <option value="USA">USA</option>
                  <option value="non-USA">Non-USA</option>
                </select>
              </div>

              <div className="space-y-1">
                <label className="text-sm font-medium text-gray-600">Engine Size (Liters)</label>
                <input type="number" step="0.1" name="EngineSize" value={formData.EngineSize} onChange={handleChange} className="w-full p-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none" required />
              </div>

              <div className="space-y-1">
                <label className="text-sm font-medium text-gray-600">Horsepower</label>
                <input type="number" name="Horsepower" value={formData.Horsepower} onChange={handleChange} className="w-full p-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none" required />
              </div>

              <div className="space-y-1">
                <label className="text-sm font-medium text-gray-600">MPG City</label>
                <input type="number" name="MPG_city" value={formData.MPG_city} onChange={handleChange} className="w-full p-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none" required />
              </div>

              <div className="space-y-1">
                <label className="text-sm font-medium text-gray-600">Weight (lbs)</label>
                <input type="number" name="Weight" value={formData.Weight} onChange={handleChange} className="w-full p-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none" required />
              </div>

              <div className="space-y-1">
                <label className="text-sm font-medium text-gray-600">AirBags</label>
                <select name="AirBags" value={formData.AirBags} onChange={handleChange} className="w-full p-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition">
                  <option value="None">None</option>
                  <option value="Driver only">Driver only</option>
                  <option value="Driver & Passenger">Driver & Passenger</option>
                </select>
              </div>

              <div className="space-y-1">
                <label className="text-sm font-medium text-gray-600">DriveTrain</label>
                <select name="DriveTrain" value={formData.DriveTrain} onChange={handleChange} className="w-full p-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition">
                  <option value="Front">Front</option>
                  <option value="Rear">Rear</option>
                  <option value="4WD">4WD</option>
                </select>
              </div>
              
              <div className="md:col-span-2 pt-4">
                <button type="submit" disabled={loading} className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-xl transition duration-200 flex justify-center items-center">
                  {loading ? 'Predicting...' : 'Predict Price'}
                </button>
              </div>
            </form>
          </div>

          {/* Right Column: Dashboard & Result */}
          <div className="space-y-6">
            
            {/* Prediction Result Card */}
            <div className="bg-gradient-to-br from-gray-900 to-gray-800 p-6 rounded-2xl shadow-lg text-white">
              <h3 className="text-lg font-medium text-gray-300 mb-2">Estimated Car Price</h3>
              <div className="flex items-center space-x-2">
                <DollarSign className="w-8 h-8 text-green-400" />
                <span className="text-4xl font-bold tracking-tight">
                  {prediction ? prediction.predicted_price.toLocaleString() : '---'}
                </span>
              </div>
              <p className="text-sm text-gray-400 mt-4 italic">
                * Estimated using a Random Forest Regression Model. Actual market prices may vary.
              </p>
            </div>

            {/* Metrics Dashboard */}
            <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
              <h3 className="text-lg font-semibold mb-4 flex items-center">
                <Activity className="w-5 h-5 mr-2 text-blue-500" />
                Model Performance
              </h3>
              
              {metrics ? (
                <div className="space-y-4">
                  <div className="flex justify-between items-center border-b border-gray-50 pb-2">
                    <span className="text-gray-500 text-sm">Model Used</span>
                    <span className="font-semibold text-gray-800">Random Forest</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-500 text-sm">Accuracy (R²)</span>
                    <span className="font-bold text-green-600 bg-green-50 px-2 py-0.5 rounded">
                      {(metrics.R2 * 100).toFixed(1)}%
                    </span>
                  </div>
                </div>
              ) : (
                <div className="text-gray-400 text-sm animate-pulse">Loading metrics from backend...</div>
              )}
            </div>
            
            <div className="bg-blue-50 p-5 rounded-xl border border-blue-100 flex items-start space-x-3">
              <Database className="text-blue-500 w-6 h-6 flex-shrink-0 mt-0.5" />
              <div>
                <h4 className="text-sm font-bold text-blue-900">Dataset Info</h4>
                <p className="text-xs text-blue-700 mt-1">Trained on the classic 1993 Cars dataset containing 93 records and 21 features. Missing values imputed.</p>
              </div>
            </div>

          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
