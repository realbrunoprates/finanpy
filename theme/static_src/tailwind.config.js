/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        '../templates/**/*.html',

        /*
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        '../../templates/**/*.html',

        /*
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        '../../**/templates/**/*.html',

        /**
         * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
         * patterns match your project structure.
         */
        /* JS 1: Ignore any JavaScript in node_modules folder. */
        // '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        // '../../**/*.js',

        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        // '../../**/*.py'
    ],
    theme: {
        extend: {
            colors: {
                // Primary gradient colors
                'primary': {
                    500: '#667eea',
                    600: '#5568d3',
                    700: '#4453bd',
                },
                'accent': {
                    500: '#764ba2',
                    600: '#63418a',
                    700: '#503672',
                },
                // Backgrounds (Dark Theme)
                'bg': {
                    'primary': '#0f172a',    // slate-900
                    'secondary': '#1e293b',  // slate-800
                    'tertiary': '#334155',   // slate-700
                },
                // Text colors
                'text': {
                    'primary': '#f1f5f9',    // slate-100
                    'secondary': '#cbd5e1',  // slate-300
                    'muted': '#64748b',      // slate-500
                },
                // Status colors
                'success': '#10b981',  // green - income
                'error': '#ef4444',    // red - expenses/errors
                'warning': '#f59e0b',  // yellow - warnings
                'info': '#3b82f6',     // blue - information
            },
        },
    },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
