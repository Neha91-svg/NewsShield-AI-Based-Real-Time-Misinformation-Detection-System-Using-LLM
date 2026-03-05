const express = require("express");
const router = express.Router();
const {
    detectNews,
    getHistory
} = require("../controllers/newsController");

router.post("/detect", detectNews);
router.get("/history", getHistory);

module.exports = router;
