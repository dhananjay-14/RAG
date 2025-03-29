const axios = require("axios");
const readline = require("readline");

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

let conversationHistory = [];

function askQuestion() {
    rl.question("Enter your question: ", async (question) => {
        if (question.toLowerCase() === "exit") {
            console.log("Exiting...");
            rl.close();
            return;
        }

        await getAnswer(question);
        askQuestion();  // Ask next question
    });
}

async function getAnswer(question) {
    try {
        const response = await axios.post("http://127.0.0.1:5000/generate-answer", {
            question: question,
            history: conversationHistory  // Send previous conversation history
        });

        console.log("Generated Answer:", response.data.answer);

        // Update conversation history (only keep last 5)
        conversationHistory.push({ question, answer: response.data.answer });
        if (conversationHistory.length > 5) {
            conversationHistory.shift();  // Remove oldest entry
        }
    } catch (error) {
        console.error("Error:", error.response ? error.response.data : error.message);
    }
}

askQuestion();

