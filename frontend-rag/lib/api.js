import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
});

export const askQuestion = async (question) => {
  const res = await api.post('/ask', { question });
  return res.data.response;
};
