import fetch from 'node-fetch';

export default async (req, res) => {
  try {
    const response = await fetch('http://ec2-3-95-219-188.compute-1.amazonaws.com:8000/chat', {
      method: req.method,
      headers: req.headers,
      body: req.body,
    });

    const contentType = response.headers.get('content-type');
    let data;
    if (contentType && contentType.includes('application/json')) {
      data = await response.json();
    } else {
      data = await response.text();
    }

    res.status(response.status).send(data);
  } catch (error) {
    res.status(500).send('Error fetching data from backend server');
  }
};
