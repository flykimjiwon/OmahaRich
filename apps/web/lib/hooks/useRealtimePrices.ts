"use client";

import { useState, useEffect, useCallback, useRef } from "react";
import type { RealtimePricesResponse, RefreshInterval } from "@/types/stock";
import { getMockRealtimePrices } from "@/lib/mock/stockData";

const BACKEND_URL = "http://localhost:8101";
const MAX_RETRY = 3;

interface UseRealtimePricesResult {
  data: RealtimePricesResponse | null;
  isLoading: boolean;
  error: string | null;
  nextUpdateIn: number; // seconds remaining until next poll
  refetch: () => void;
  isStale: boolean;
}

export function useRealtimePrices(interval: RefreshInterval): UseRealtimePricesResult {
  const [data, setData] = useState<RealtimePricesResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [nextUpdateIn, setNextUpdateIn] = useState<number>(interval);
  const [isStale, setIsStale] = useState(false);

  const retryCount = useRef(0);
  const lastFetchedAt = useRef<number | null>(null);
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const countdownRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const fetchPrices = useCallback(async () => {
    setIsLoading(true);
    try {
      const res = await fetch(`${BACKEND_URL}/api/v1/realtime/prices`, {
        signal: AbortSignal.timeout(8000),
      });
      if (!res.ok) {
        throw new Error(`서버 응답 오류: ${res.status}`);
      }
      const json: RealtimePricesResponse = await res.json();
      setData(json);
      setError(null);
      setIsStale(false);
      retryCount.current = 0;
      lastFetchedAt.current = Date.now();
    } catch (err) {
      retryCount.current += 1;
      const isBacked = retryCount.current <= MAX_RETRY;
      if (isBacked) {
        // 백엔드 미연결 — Mock 데이터로 레이아웃 확인
        const mock = getMockRealtimePrices();
        setData(mock);
        setIsStale(false);
        setError("서버 연결 중... (Mock 데이터 표시)");
      } else {
        const msg = err instanceof Error ? err.message : "알 수 없는 오류";
        setError(`데이터 로드 실패: ${msg}`);
        setIsStale(true);
      }
      lastFetchedAt.current = Date.now();
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Countdown timer
  const startCountdown = useCallback(() => {
    if (countdownRef.current) clearInterval(countdownRef.current);
    setNextUpdateIn(interval);
    let remaining = interval;
    countdownRef.current = setInterval(() => {
      remaining -= 1;
      setNextUpdateIn(remaining);
      if (remaining <= 0) {
        if (countdownRef.current) clearInterval(countdownRef.current);
      }
    }, 1000);
  }, [interval]);

  // Initial fetch + polling
  useEffect(() => {
    fetchPrices();
    startCountdown();

    if (intervalRef.current) clearInterval(intervalRef.current);
    intervalRef.current = setInterval(() => {
      fetchPrices();
      startCountdown();
    }, interval * 1000);

    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
      if (countdownRef.current) clearInterval(countdownRef.current);
    };
  }, [interval, fetchPrices, startCountdown]);

  // Mark stale if last fetch was too long ago
  useEffect(() => {
    const staleness = setInterval(() => {
      if (lastFetchedAt.current !== null) {
        const elapsed = (Date.now() - lastFetchedAt.current) / 1000;
        if (elapsed > interval * 3) {
          setIsStale(true);
        }
      }
    }, 5000);
    return () => clearInterval(staleness);
  }, [interval]);

  const refetch = useCallback(() => {
    if (intervalRef.current) clearInterval(intervalRef.current);
    fetchPrices();
    startCountdown();
    intervalRef.current = setInterval(() => {
      fetchPrices();
      startCountdown();
    }, interval * 1000);
  }, [fetchPrices, startCountdown, interval]);

  return { data, isLoading, error, nextUpdateIn, refetch, isStale };
}
