/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./app/templates/**/*.html", // Flask templates
        "./app/static/src/**/*.js", // Any custom JS in src/
        "./node_modules/flowbite/**/*.js", // Flowbite files
    ],
    theme: {
        extend: {},
    },
    plugins: [
        require("flowbite/plugin"), // Include Flowbite plugin
    ],
};
