import React, { useState } from 'react';

const Frontend = () => {
  const [formData, setFormData] = useState({
    principal: '',
    coupon_rate: '',
    ytm: '',
    maturity_date: ''
  });

  const [results, setResults] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await fetch('http://localhost:8000/calculate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          principal: parseFloat(formData.principal),
          coupon_rate: parseFloat(formData.coupon_rate),
          ytm: parseFloat(formData.ytm),
          maturity_date: formData.maturity_date
        })
      });

      if (!response.ok) {
        throw new Error('Calculation error');
      }

      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError('An error occurred during calculation. Please check your inputs.');
    } finally {
      setLoading(false);
    }
  };

  const formatNumber = (num) => {
    return Number(num).toFixed(4);
  };

  return (
    <div className="container mx-auto p-4 max-w-2xl">
      <div className="bg-white rounded-lg shadow-md p-6">
        <h1 className="text-2xl font-bold text-center mb-6">Bond Calculator</h1>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Principal (€)
            </label>
            <input
              type="number"
              name="principal"
              value={formData.principal}
              onChange={handleInputChange}
              placeholder="E.g., 1000"
              required
              step="0.01"
              className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Coupon Rate (%)
            </label>
            <input
              type="number"
              name="coupon_rate"
              value={formData.coupon_rate}
              onChange={handleInputChange}
              placeholder="E.g., 5"
              required
              step="0.01"
              className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Yield to Maturity (%)
            </label>
            <input
              type="number"
              name="ytm"
              value={formData.ytm}
              onChange={handleInputChange}
              placeholder="E.g., 6"
              required
              step="0.01"
              className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Maturity Date
            </label>
            <input
              type="date"
              name="maturity_date"
              value={formData.maturity_date}
              onChange={handleInputChange}
              required
              className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          <button 
            type="submit" 
            className="w-full bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:bg-blue-300"
            disabled={loading}
          >
            {loading ? 'Calculating...' : 'Calculate'}
          </button>
        </form>

        {error && (
          <div className="mt-4 p-4 bg-red-50 text-red-600 rounded-md">
            {error}
          </div>
        )}

        {results && (
          <div className="mt-6">
            <h3 className="text-lg font-semibold mb-4">Results</h3>
            <div className="grid grid-cols-2 gap-4">
              <div className="p-3 bg-gray-50 rounded-md">
                <p className="text-sm text-gray-600">Clean Price</p>
                <p className="text-lg font-medium">{formatNumber(results.clean_price)} €</p>
              </div>
              <div className="p-3 bg-gray-50 rounded-md">
                <p className="text-sm text-gray-600">Dirty Price</p>
                <p className="text-lg font-medium">{formatNumber(results.dirty_price)} €</p>
              </div>
              <div className="p-3 bg-gray-50 rounded-md">
                <p className="text-sm text-gray-600">Modified Duration</p>
                <p className="text-lg font-medium">{formatNumber(results.modified_duration)}</p>
              </div>
              <div className="p-3 bg-gray-50 rounded-md">
                <p className="text-sm text-gray-600">Convexity</p>
                <p className="text-lg font-medium">{formatNumber(results.convexity)}</p>
              </div>
              <div className="p-3 bg-gray-50 rounded-md">
                <p className="text-sm text-gray-600">Elasticity</p>
                <p className="text-lg font-medium">{formatNumber(results.elasticity)}</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Frontend;