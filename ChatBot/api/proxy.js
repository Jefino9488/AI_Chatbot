import { createProxyMiddleware } from 'http-proxy-middleware';

export default (req, res) => {
  const proxy = createProxyMiddleware({
    target: 'http://ec2-3-87-174-179.compute-1.amazonaws.com:8000',
    changeOrigin: true,
    pathRewrite: { '^/api': '' },
    secure: false,
  });
  proxy(req, res, () => {});
};
