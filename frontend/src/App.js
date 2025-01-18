import Frontend from './components/Frontend';
import ChatComponent from './components/ChatComponent';

function App() {
  return (
    <div className="min-h-screen bg-gray-100">
      <div className="container mx-auto py-8">
        <Frontend />
        <div className="mt-8">
          <ChatComponent />
        </div>
      </div>
    </div>
  );
}

export default App;