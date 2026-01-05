import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  ActivityIndicator,
  Alert,
  Platform,
} from 'react-native';
import { StatusBar } from 'expo-status-bar';
import * as ImagePicker from 'expo-image-picker';
import * as DocumentPicker from 'expo-document-picker';
import * as Clipboard from 'expo-clipboard';
import * as FileSystem from 'expo-file-system';
import * as Sharing from 'expo-sharing';
import * as TextExtractor from 'expo-text-extractor';
import { Ionicons } from '@expo/vector-icons';
import Constants from 'expo-constants';

export default function HomeScreen() {
  const [extractedText, setExtractedText] = useState('');
  const [loading, setLoading] = useState(false);
  const [imageUri, setImageUri] = useState<string | null>(null);

  const BACKEND_URL = Constants.expoConfig?.extra?.EXPO_BACKEND_URL || process.env.EXPO_BACKEND_URL || 'http://localhost:8001';

  // Request permissions
  const requestPermissions = async () => {
    const { status: cameraStatus } = await ImagePicker.requestCameraPermissionsAsync();
    const { status: mediaStatus } = await ImagePicker.requestMediaLibraryPermissionsAsync();
    
    if (cameraStatus !== 'granted' || mediaStatus !== 'granted') {
      Alert.alert('Permissions Required', 'Please grant camera and media library permissions to use this app.');
      return false;
    }
    return true;
  };

  // Process image with OCR
  const processImage = async (uri: string) => {
    try {
      setLoading(true);
      setImageUri(uri);

      // Check if text extraction is supported
      const isSupported = await TextExtractor.isSupported();
      if (!isSupported) {
        Alert.alert('Not Supported', 'Text extraction is not supported on this device.');
        return;
      }

      // Extract text from image
      const result = await TextExtractor.extractTextFromImage(uri);
      
      if (result && result.length > 0) {
        const text = result.join('\n');
        setExtractedText(text);
      } else {
        Alert.alert('No Text Found', 'Could not extract any text from this image.');
        setExtractedText('');
      }
    } catch (error) {
      console.error('OCR Error:', error);
      Alert.alert('Error', 'Failed to extract text from image.');
    } finally {
      setLoading(false);
    }
  };

  // Capture photo with camera
  const capturePhoto = async () => {
    const hasPermission = await requestPermissions();
    if (!hasPermission) return;

    try {
      const result = await ImagePicker.launchCameraAsync({
        mediaTypes: ['images'],
        quality: 1,
        allowsEditing: false,
      });

      if (!result.canceled && result.assets[0]) {
        await processImage(result.assets[0].uri);
      }
    } catch (error) {
      console.error('Camera Error:', error);
      Alert.alert('Error', 'Failed to capture photo.');
    }
  };

  // Pick image from gallery
  const pickImage = async () => {
    const hasPermission = await requestPermissions();
    if (!hasPermission) return;

    try {
      const result = await ImagePicker.launchImageLibraryAsync({
        mediaTypes: ['images'],
        quality: 1,
        allowsEditing: false,
      });

      if (!result.canceled && result.assets[0]) {
        await processImage(result.assets[0].uri);
      }
    } catch (error) {
      console.error('Gallery Error:', error);
      Alert.alert('Error', 'Failed to pick image.');
    }
  };

  // Pick and process PDF
  const pickPDF = async () => {
    try {
      const result = await DocumentPicker.getDocumentAsync({
        type: 'application/pdf',
        copyToCacheDirectory: true,
      });

      if (!result.canceled && result.assets[0]) {
        Alert.alert(
          'PDF Processing',
          'PDF text extraction requires converting pages to images first. This feature is limited in the current offline implementation. Please use image screenshots of PDF pages instead.'
        );
      }
    } catch (error) {
      console.error('PDF Error:', error);
      Alert.alert('Error', 'Failed to process PDF.');
    }
  };

  // Copy text to clipboard
  const copyToClipboard = async () => {
    if (!extractedText) {
      Alert.alert('No Text', 'No text to copy.');
      return;
    }

    try {
      await Clipboard.setStringAsync(extractedText);
      Alert.alert('Copied!', 'Text copied to clipboard.');
    } catch (error) {
      Alert.alert('Error', 'Failed to copy text.');
    }
  };

  // Download as TXT file
  const downloadAsTXT = async () => {
    if (!extractedText) {
      Alert.alert('No Text', 'No text to download.');
      return;
    }

    try {
      const filename = `extracted_text_${Date.now()}.txt`;
      const fileUri = `${FileSystem.documentDirectory}${filename}`;
      
      await FileSystem.writeAsStringAsync(fileUri, extractedText);
      
      if (await Sharing.isAvailableAsync()) {
        await Sharing.shareAsync(fileUri);
      } else {
        Alert.alert('Success', `File saved to: ${fileUri}`);
      }
    } catch (error) {
      console.error('TXT Download Error:', error);
      Alert.alert('Error', 'Failed to save TXT file.');
    }
  };

  // Download as DOCX file
  const downloadAsDOCX = async () => {
    if (!extractedText) {
      Alert.alert('No Text', 'No text to download.');
      return;
    }

    try {
      setLoading(true);
      const filename = `extracted_text_${Date.now()}.docx`;

      // Call backend API to generate DOCX
      const response = await fetch(`${BACKEND_URL}/api/generate-docx`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: extractedText,
          filename: filename,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to generate DOCX');
      }

      // Get blob and save
      const blob = await response.blob();
      const reader = new FileReader();
      
      reader.onloadend = async () => {
        const base64data = reader.result as string;
        const base64 = base64data.split(',')[1];
        
        const fileUri = `${FileSystem.documentDirectory}${filename}`;
        await FileSystem.writeAsStringAsync(fileUri, base64, {
          encoding: FileSystem.EncodingType.Base64,
        });
        
        if (await Sharing.isAvailableAsync()) {
          await Sharing.shareAsync(fileUri);
        } else {
          Alert.alert('Success', `File saved to: ${fileUri}`);
        }
      };
      
      reader.readAsDataURL(blob);
    } catch (error) {
      console.error('DOCX Download Error:', error);
      Alert.alert('Error', 'Failed to generate DOCX file.');
    } finally {
      setLoading(false);
    }
  };

  // Clear all data
  const clearAll = () => {
    setExtractedText('');
    setImageUri(null);
  };

  return (
    <View style={styles.container}>
      <StatusBar style="light" />
      
      {/* Header */}
      <View style={styles.header}>
        <Ionicons name="document-text" size={40} color="#fff" />
        <Text style={styles.headerTitle}>OCR Text Extractor</Text>
        <Text style={styles.headerSubtitle}>Offline • No History Saved</Text>
      </View>

      <ScrollView style={styles.content} contentContainerStyle={styles.contentContainer}>
        {/* Action Buttons */}
        {!extractedText && (
          <View style={styles.actionSection}>
            <Text style={styles.sectionTitle}>Select Input Source</Text>
            
            <TouchableOpacity style={styles.actionButton} onPress={capturePhoto}>
              <Ionicons name="camera" size={32} color="#4CAF50" />
              <Text style={styles.actionButtonText}>Take Photo</Text>
              <Text style={styles.actionButtonSubtext}>Capture with camera</Text>
            </TouchableOpacity>

            <TouchableOpacity style={styles.actionButton} onPress={pickImage}>
              <Ionicons name="images" size={32} color="#2196F3" />
              <Text style={styles.actionButtonText}>Upload Image</Text>
              <Text style={styles.actionButtonSubtext}>Choose from gallery</Text>
            </TouchableOpacity>

            <TouchableOpacity style={styles.actionButton} onPress={pickPDF}>
              <Ionicons name="document" size={32} color="#FF9800" />
              <Text style={styles.actionButtonText}>Upload PDF</Text>
              <Text style={styles.actionButtonSubtext}>Extract from document</Text>
            </TouchableOpacity>
          </View>
        )}

        {/* Loading Indicator */}
        {loading && (
          <View style={styles.loadingContainer}>
            <ActivityIndicator size="large" color="#4CAF50" />
            <Text style={styles.loadingText}>Processing...</Text>
          </View>
        )}

        {/* Extracted Text Display */}
        {extractedText && !loading && (
          <View style={styles.resultSection}>
            <View style={styles.resultHeader}>
              <Text style={styles.sectionTitle}>Extracted Text</Text>
              <TouchableOpacity onPress={clearAll} style={styles.clearButton}>
                <Ionicons name="close-circle" size={24} color="#f44336" />
              </TouchableOpacity>
            </View>

            <View style={styles.textContainer}>
              <ScrollView style={styles.textScroll}>
                <Text style={styles.extractedText}>{extractedText}</Text>
              </ScrollView>
            </View>

            {/* Export Options */}
            <View style={styles.exportSection}>
              <Text style={styles.exportTitle}>Export Options</Text>
              
              <View style={styles.exportButtons}>
                <TouchableOpacity style={styles.exportButton} onPress={copyToClipboard}>
                  <Ionicons name="copy" size={24} color="#fff" />
                  <Text style={styles.exportButtonText}>Copy</Text>
                </TouchableOpacity>

                <TouchableOpacity style={styles.exportButton} onPress={downloadAsTXT}>
                  <Ionicons name="document-text" size={24} color="#fff" />
                  <Text style={styles.exportButtonText}>TXT</Text>
                </TouchableOpacity>

                <TouchableOpacity style={styles.exportButton} onPress={downloadAsDOCX}>
                  <Ionicons name="document" size={24} color="#fff" />
                  <Text style={styles.exportButtonText}>DOCX</Text>
                </TouchableOpacity>
              </View>
            </View>
          </View>
        )}

        {/* Info Section */}
        {!extractedText && !loading && (
          <View style={styles.infoSection}>
            <Ionicons name="information-circle" size={24} color="#666" />
            <Text style={styles.infoText}>
              This app uses on-device OCR (Google ML Kit on Android, Apple Vision on iOS) for offline text extraction.
            </Text>
            <Text style={styles.infoText}>
              Works best with clear, well-lit images and printed text. Handwriting recognition is limited.
            </Text>
          </View>
        )}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    backgroundColor: '#4CAF50',
    paddingTop: 60,
    paddingBottom: 30,
    paddingHorizontal: 20,
    alignItems: 'center',
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
    marginTop: 12,
  },
  headerSubtitle: {
    fontSize: 14,
    color: '#e8f5e9',
    marginTop: 4,
  },
  content: {
    flex: 1,
  },
  contentContainer: {
    padding: 20,
  },
  actionSection: {
    marginBottom: 20,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
    marginBottom: 16,
  },
  actionButton: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 20,
    marginBottom: 12,
    flexDirection: 'row',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  actionButtonText: {
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
    marginLeft: 16,
    flex: 1,
  },
  actionButtonSubtext: {
    fontSize: 12,
    color: '#999',
    position: 'absolute',
    left: 68,
    bottom: 18,
  },
  loadingContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    padding: 40,
  },
  loadingText: {
    marginTop: 12,
    fontSize: 16,
    color: '#666',
  },
  resultSection: {
    flex: 1,
  },
  resultHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  clearButton: {
    padding: 4,
  },
  textContainer: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    marginBottom: 20,
    maxHeight: 300,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  textScroll: {
    maxHeight: 280,
  },
  extractedText: {
    fontSize: 15,
    color: '#333',
    lineHeight: 22,
  },
  exportSection: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  exportTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginBottom: 16,
  },
  exportButtons: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  exportButton: {
    backgroundColor: '#4CAF50',
    borderRadius: 8,
    padding: 16,
    flex: 1,
    marginHorizontal: 4,
    alignItems: 'center',
  },
  exportButtonText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: '600',
    marginTop: 4,
  },
  infoSection: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 20,
    alignItems: 'center',
    marginTop: 20,
  },
  infoText: {
    fontSize: 14,
    color: '#666',
    textAlign: 'center',
    marginTop: 8,
    lineHeight: 20,
  },
});