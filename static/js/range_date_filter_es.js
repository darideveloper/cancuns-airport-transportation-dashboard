// Update placeholder text for unfold range date filter

// Run after page loads
document.addEventListener("DOMContentLoaded", function () {
  const texts = [
    {
      ids: ["created_at_from", "updated_at_from"],
      text: "Desde",
    },
    {
      ids: ["created_at_to", "updated_at_to"],
      text: "Hasta",
    },
  ]

  texts.forEach((text) => {
    text.ids.forEach((id) => {
      const elem = document.querySelector(`#${id}`)
      if (!elem) return
      elem.placeholder = text.text
    })
  })
})