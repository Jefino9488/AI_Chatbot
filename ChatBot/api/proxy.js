import fetch from 'node-fetch';

export default async (req, res) => {
  const response = await fetch('http://ec2-3-95-219-188.compute-1.amazonaws.com:8000/chat', {
    method: req.method,
    headers: req.headers,
    body: req.body,
  });

  const data = await response.text();
  res.status(response.status).send(data);
};
