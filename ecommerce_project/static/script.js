document.querySelectorAll('.quantity-btn').forEach(button => {
  button.addEventListener('click', function() {
    const action = this.dataset.action;
    const input = this.parentNode.querySelector('.quantity-input');
    let quantity = parseInt(input.value);
      
    if (action === 'increase') {
        quantity += 1;
    } else if (action === 'decrease' && quantity > 1) {
      quantity -= 1;
    }
      
    input.value = quantity;
  });
});

document.getElementById('logout-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const form = e.target;
    const response = await fetch(form.action, {
        method: 'POST',
        headers: {
            'X-CSRFToken': form.csrfmiddlewaretoken.value,
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `csrfmiddlewaretoken=${form.csrfmiddlewaretoken.value}&next=${form.next.value}`,
        credentials: 'include'
    });
    if (response.redirected) window.location = response.url;
});