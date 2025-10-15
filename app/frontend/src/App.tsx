import { TimeRequest } from '@/components/TimeRequest';

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto py-8 px-4">
        <header className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            TWS Integration Dashboard
          </h1>
          <p className="text-gray-600 text-lg">
            Interactive Trader Workstation frontend application
          </p>
        </header>

        <main className="max-w-4xl mx-auto">
          <div className="grid gap-6">
            <section>
              <h2 className="text-2xl font-semibold mb-4">Time Service</h2>
              <TimeRequest />
            </section>
          </div>
        </main>

        <footer className="text-center mt-12 text-sm text-gray-600">
          <p>Built with React, TypeScript, Vite, and shadcn/ui</p>
        </footer>
      </div>
    </div>
  );
}

export default App;