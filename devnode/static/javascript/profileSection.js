let userData=[];
async function getfxn(){
  let res= await fetch("http://127.0.0.1:5000/profiles_api/", {
      "method": "GET"
      })
  let resObj=await res.json();
   console.log(resObj.data);
  userData= resObj.data;
  document.getElementById("cards").innerHTML=`
  ${userData.map((user)=>{userCard(user)}).join("")}hwllo
  `;
}
getfxn()
function userCard(user) {
    return `
    <div class="profile-card">
    <div class="profile-image" style="background-image:url(${user.cover_pic})"><img src="${user.profile_pic}" alt="${user.username}" width=200/></div>
    <figcaption>
      <h3>${user.username}</h3>
      <h5>${user.designation}</h5>
    
      <div class="icons">
        <a href="https://gmail.com/${user.email}"><img src="	https://cdn.icon-icons.com/icons2/2201/PNG/512/gmail_logo_round_icon_134018.png"/ style="height:52px;"></a>
        <a href="https://linkedin.com/in/${user.linkedin_id}"> <img src="https://img.icons8.com/color/48/000000/linkedin-circled.png"/></a>
        <a href="https://github.com/in/${user.github_id}"> <img src="https://img.icons8.com/material-outlined/48/000000/github.png"/></a>
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
      let name = user.username;
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