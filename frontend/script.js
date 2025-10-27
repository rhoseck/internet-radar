const input = document.getElementById("ideaInput");
const button = document.getElementById("addIdea");
const list = document.getElementById("ideaList");

let ideas = JSON.parse(localStorage.getItem("ideas")) || [];

function displayIdeas() {
  list.innerHTML = "";
  ideas.forEach((idea, index) => {
    const li = document.createElement("li");
    li.textContent = idea;
    
    // Delete button
    const delBtn = document.createElement("button");
    delBtn.textContent = "x";
    delBtn.onclick = () => {
      ideas.splice(index, 1);
      localStorage.setItem("ideas", JSON.stringify(ideas));
      displayIdeas();
    };
    
    li.appendChild(delBtn);
    list.appendChild(li);
  });
}

button.onclick = () => {
  const idea = input.value.trim();
  if (idea) {
    ideas.push(idea);
    localStorage.setItem("ideas", JSON.stringify(ideas));
    displayIdeas();
    input.value = "";
  }
};

displayIdeas();
