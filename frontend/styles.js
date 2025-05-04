// styles.js
import { StyleSheet, Platform } from 'react-native';

const styles = StyleSheet.create({
  container: {
    padding: 24,
    backgroundColor: '#f0f4f8',
    flexGrow: 1,
    marginTop: Platform.OS === 'ios' ? 60 : 40,
  },
  header: {
    backgroundColor: '#0077b6',
    padding: 20,
    borderRadius: 12,
    marginBottom: 20,
    alignItems: 'center',
  },
  title: {
    fontSize: 26,
    fontWeight: 'bold',
    color: '#fff',
  },
  subtitle: {
    fontSize: 14,
    color: '#d0e8f2',
    marginTop: 6,
    textAlign: 'center',
  },
  card: {
    backgroundColor: '#ffffff',
    borderRadius: 12,
    padding: 20,
    shadowColor: '#000',
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 4,
  },
  label: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 10,
    color: '#333',
  },
  input: {
    minHeight: 80,
    borderColor: '#ccc',
    borderWidth: 1,
    borderRadius: 10,
    paddingHorizontal: 12,
    paddingVertical: 10,
    backgroundColor: '#fafafa',
    textAlignVertical: 'top',
    marginBottom: 15,
  },
  button: {
    backgroundColor: '#00b4d8',
    paddingVertical: 12,
    borderRadius: 10,
    alignItems: 'center',
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  responseCard: {
    marginTop: 20,
    backgroundColor: '#caf0f8',
    padding: 18,
    borderRadius: 12,
    borderColor: '#90e0ef',
    borderWidth: 1,
  },
  responseLabel: {
    fontSize: 15,
    fontWeight: 'bold',
    color: '#0077b6',
    marginBottom: 8,
  },
  responseText: {
    fontSize: 16,
    color: '#023e8a',
  },
});

export default styles;
