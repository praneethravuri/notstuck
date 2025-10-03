import { useState, useEffect } from "react";

export function useBackendHealth() {
    const [isBackendReady, setIsBackendReady] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        let isMounted = true;
        let retryCount = 0;
        const maxRetries = 30; // 30 seconds max wait time

        const checkBackendHealth = async () => {
            try {
                const response = await fetch("/api/health", {
                    method: "GET",
                    cache: "no-cache",
                });

                if (response.ok && isMounted) {
                    setIsBackendReady(true);
                    setError(null);
                } else {
                    throw new Error(`Health check failed: ${response.status}`);
                }
            } catch (err) {
                if (!isMounted) return;

                retryCount++;
                if (retryCount >= maxRetries) {
                    setError("Backend failed to start after 30 seconds. Please check your backend server.");
                    return;
                }

                // Retry after 1 second
                setTimeout(checkBackendHealth, 1000);
            }
        };

        checkBackendHealth();

        return () => {
            isMounted = false;
        };
    }, []);

    return { isBackendReady, error };
}
