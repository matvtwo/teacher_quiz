document.addEventListener("DOMContentLoaded", () => {
  const btn = document.createElement("button");
  btn.type = "button";
  btn.innerText = "Сгенерировать через ИИ";
  btn.style.margin = "10px 0";

  const q = document.querySelector("#id_text");
  if (!q) return;

  q.parentNode.insertBefore(btn, q);

  btn.onclick = async () => {
    btn.disabled = true;
    btn.innerText = "Генерация...";
    const res = await fetch("/admin/ai/generate-question/");
    const data = await res.json();
    document.querySelector("#id_text").value = data.question;
    document.querySelector("#id_option_a").value = data.options[0];
    document.querySelector("#id_option_b").value = data.options[1];
    document.querySelector("#id_option_c").value = data.options[2];
    document.querySelector("#id_option_d").value = data.options[3];
    document.querySelector("#id_correct_answer").value = data.correct;
    btn.innerText = "Сгенерировать через ИИ";
    btn.disabled = false;
  };
});
