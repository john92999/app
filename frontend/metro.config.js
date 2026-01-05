// metro.config.js
const { getDefaultConfig } = require("expo/metro-config");

/** @type {import('expo/metro-config').MetroConfig} */
const config = getDefaultConfig(__dirname);

// SAFE CACHE SETTING FOR EAS
// We remove the manual FileStore configuration.
// This allows Metro to use the system's temporary directory
// or memory, which avoids "Permission Denied" errors.
config.cacheStores = [];

// Keep your performance optimization
config.maxWorkers = 2;

module.exports = config;
