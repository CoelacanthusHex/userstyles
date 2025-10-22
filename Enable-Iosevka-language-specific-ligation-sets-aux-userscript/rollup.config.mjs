import babelPlugin from '@rollup/plugin-babel';
import commonjsPlugin from '@rollup/plugin-commonjs';
import jsonPlugin from '@rollup/plugin-json';
import resolvePlugin from '@rollup/plugin-node-resolve';
import replacePlugin from '@rollup/plugin-replace';
import { readPackageUp } from 'read-package-up';
import { defineConfig } from 'rollup';
import userscript from 'rollup-plugin-userscript';

const { packageJson } = await readPackageUp();
const extensions = ['.ts', '.tsx', '.mjs', '.js', '.jsx'];

export default defineConfig(
  Object.entries({
    'Enable-Iosevka-language-specific-ligation-sets-aux-userscript': 'src/index.ts',
  }).map(([name, entry]) => ({
    input: entry,
    plugins: [
      babelPlugin({
        // import helpers from '@babel/runtime'
        babelHelpers: 'runtime',
        plugins: [
          [
            import.meta.resolve('@babel/plugin-transform-runtime'),
            {
              useESModules: true,
              version: '^7.5.0', // see https://github.com/babel/babel/issues/10261#issuecomment-514687857
            },
          ],
        ],
        exclude: 'node_modules/**',
        extensions,
      }),
      replacePlugin({
        values: {
          'process.env.NODE_ENV': JSON.stringify(process.env.NODE_ENV),
        },
        preventAssignment: true,
      }),
      resolvePlugin({ browser: false, extensions }),
      commonjsPlugin(),
      jsonPlugin(),
      userscript((meta) =>
        meta.replace('process.env.AUTHOR', packageJson.author.name),
      ),
    ],
    output: {
      format: 'es',
      file: `dist/${name}.user.js`,
      indent: false,
    },
  })),
);
