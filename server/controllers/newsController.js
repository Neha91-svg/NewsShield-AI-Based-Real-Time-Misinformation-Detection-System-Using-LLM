const axios = require("axios");
const Prediction = require("../models/Prediction");

exports.detectNews = async (req, res) => {
  try {
    const { text } = req.body;

    const aiRes = await axios.post(process.env.AI_URL, { text });

    const saved = await Prediction.create({
      text,
      prediction: aiRes.data.prediction,
      confidence: aiRes.data.confidence
    });

    res.json(saved);
  } catch (err) {
    res.status(500).json({ error: "Detection failed" });
  }
};

exports.getHistory = async (req, res) => {
  const history = await Prediction.find().sort({ createdAt: -1 });
  res.json(history);
};