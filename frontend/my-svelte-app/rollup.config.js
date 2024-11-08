import svelte from 'rollup-plugin-svelte';
import commonjs from '@rollup/plugin-commonjs';
import resolve from '@rollup/plugin-node-resolve';
import json from '@rollup/plugin-json';
import livereload from 'rollup-plugin-livereload';
import terser from '@rollup/plugin-terser';
import css from 'rollup-plugin-css-only';
import serve from 'rollup-plugin-serve';
import replace from '@rollup/plugin-replace'; // 플러그인 추가

const production = !process.env.ROLLUP_WATCH;

export default {
    input: 'src/main.js',
    output: {
        sourcemap: true,
        format: 'esm',
        dir: 'public/build',
    },
    plugins: [
        replace({
            preventAssignment: true, // 이 옵션을 추가해야 경고 없이 실행됩니다.
            'process.env.OPENAI_API_KEY': JSON.stringify(process.env.OPENAI_API_KEY)
        }),
        svelte({
            compilerOptions: {
                dev: !production
            }
        }),
        css({ output: 'bundle.css' }),
        json(),
        resolve({
            browser: true,
            dedupe: ['svelte']
        }),
        commonjs(),
        !production && serve({
            contentBase: 'public',
            port: 5000,
            historyApiFallback: true,
        }),
        !production && livereload('public'),
        production && terser()
    ],
    watch: {
        clearScreen: false
    }
};
