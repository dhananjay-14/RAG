const axios = require("axios");
const readline = require("readline");

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

rl.question("Enter your question: ", async (question) => {
    await getAnswer(question);
    rl.close();
});

async function getAnswer(question) {
    try {
        const response = await axios.post("http://127.0.0.1:5000/generate-answer", {
            question: question,
        });

        console.log("Generated Answer:", response.data.answer);
    } catch (error) {
        console.error("Error:", error.response ? error.response.data : error.message);
    }
}

