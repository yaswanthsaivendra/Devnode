function userCard(user) {
    return `
    <div class="profile-card">
    <div class="profile-image" style="background-image:url(${user.userCover})"><img src="${user.userImage}" alt="${user.userName}" width=200/></div>
    <figcaption>
      <h3>${user.userName}</h3>
      <h5>${user.userDesignation}</h5>
    
      <div class="icons">
        <a href="https://gmail.com/${user.mailID}"><img src="	https://cdn.icon-icons.com/icons2/2201/PNG/512/gmail_logo_round_icon_134018.png"/ style="height:52px;"></a>
        <a href="https://linkedin.com/in/${user.linkedinID}"> <img src="https://img.icons8.com/color/48/000000/linkedin-circled.png"/></a>
        <a href="https://github.com/in/${user.githubID}"> <img src="https://img.icons8.com/material-outlined/48/000000/github.png"/></a>
      </div>
      </figcaption>
    </div>
  `;
  }
  let userRender = [];
  document.getElementById("cards").innerHTML = `
  ${userData.map(userCard).join("")}
  `;
  //onInput
  let inputField = document.getElementById("inputField");
  let inputText = inputField.value;
  inputField.addEventListener("input", () => {
    inputText = inputField.value;
    SearchFxn();
  });
  //on button click
  let btn = document.getElementById("btn");
  btn.addEventListener("click", (e) => {
    e.preventDefault();
    inputText = inputField.value;
    SearchFxn();
  });
  //function to filter out
  function SearchFxn() {
    userRender = [];
    userData.map((user, i) => {
      let name = user.userName;
      name = name.toLowerCase();
      if (name.includes(inputText)) {
        userRender = [...userRender, user];
        userRender = [...new Set(userRender)];
      }
    });
    document.getElementById("cards").innerHTML = `
  ${userRender.map(userCard).join("")}
  `;
  }