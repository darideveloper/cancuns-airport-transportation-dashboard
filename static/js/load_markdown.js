// Runs script when page loads
document.addEventListener("DOMContentLoaded", () => {
  // Get text areas
  const noMarkdownIds = [
    "google_maps_src", // Property google maps src field
    "description", // Post description field
  ]
  let textAreasSelector = 'div > textarea'
  const notSelector = noMarkdownIds.map(id => `:not(#id_${id})`).join("")
  textAreasSelector = `div > textarea${notSelector}`
  const textAreas = document.querySelectorAll(textAreasSelector)
  console.log({ textAreas })

  setTimeout(() => {
    textAreas.forEach(textArea => {
      new SimpleMDE({
        element: textArea,
        toolbar: [
          "bold", "italic", "heading", "|",
          "quote", "code", "link", "image", "|",
          "unordered-list", "ordered-list", "|",
          "undo", "redo", "|",
          "preview",
        ],
        spellChecker: false,
      })
    })
  }, 100)
})