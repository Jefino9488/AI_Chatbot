import fetch from 'node-fetch';

export default async (req, res) => {
  try {
    const formData = new FormData();

    for (const key in req.body) {
      formData.append(key, req.body[key]);
    }

    if (req.body.file) {
      formData.append('file', req.body.file);
    }

    const response = await fetch('http://ec2-3-95-219-188.compute-1.amazonaws.com:8000/chat', {
      method: 'POST',
      headers: {
        'Content-Type': req.headers['content-type'],
        ...req.headers,
      },
      body: formData,
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
    console.error('Error:', error);
    res.status(500).send('Error fetching data from backend server');
  }
};
