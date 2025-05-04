import { StatusBar } from 'expo-status-bar';
import React, { useState } from 'react';
import {
  Text,
  TextInput,
  View,
  TouchableOpacity,
  ScrollView,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import styles from './styles'; // Make sure this path is correct based on your folder structure

export default function App() {
  const [inputText, setInputText] = useState('');
  const [responseText, setResponseText] = useState('');

  const handleSend = async () => {
    try {
      const res = await fetch('http://192.168.100.38:8000/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: inputText }),
      });

      const data = await res.json();
      setResponseText(data.answer || 'No response from server');
    } catch (error) {
      console.error(error);
      setResponseText('Error connecting to server');
    }
  };

  return (
    <KeyboardAvoidingView
      style={{ flex: 1 }}
      behavior={Platform.OS === 'ios' ? 'padding' : undefined}
    >
      <ScrollView contentContainerStyle={styles.container}>
        <View style={styles.header}>
          <Text style={styles.title}>🧳 Visa Assistant</Text>
          <Text style={styles.subtitle}>
            Accurate visa & residency answers for digital nomads
          </Text>
        </View>

        <View style={styles.card}>
          <Text style={styles.label}>Ask a Question</Text>
          <TextInput
            style={styles.input}
            placeholder="e.g., Can I take my spouse to Spain under the DNV?"
            value={inputText}
            onChangeText={setInputText}
            multiline
          />

          <TouchableOpacity style={styles.button} onPress={handleSend}>
            <Text style={styles.buttonText}>Send</Text>
          </TouchableOpacity>
        </View>

        {responseText !== '' && (
          <View style={styles.responseCard}>
            <Text style={styles.responseLabel}>Bot Response:</Text>
            <Text style={styles.responseText}>{responseText}</Text>
          </View>
        )}

        <StatusBar style="auto" />
      </ScrollView>
    </KeyboardAvoidingView>
  );
}
