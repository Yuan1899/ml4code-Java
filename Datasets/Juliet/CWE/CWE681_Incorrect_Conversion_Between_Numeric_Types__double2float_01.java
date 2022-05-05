/* TEMPLATE GENERATED TESTCASE FILE
Filename: CWE681_Incorrect_Conversion_Between_Numeric_Types__double2float_01.java
Label Definition File: CWE681_Incorrect_Conversion_Between_Numeric_Types.label.xml
Template File: point-flaw-01.tmpl.java
*/
/*
* @description
* CWE: 681 Incorrect Conversion Between Numeric Types
* Sinks: double2float
*    GoodSink: check for conversion error
*    BadSink : explicit cast
* Flow Variant: 01 Baseline
*
* */






import java.io.*;

import java.util.logging.Level;

public class CWE681_Incorrect_Conversion_Between_Numeric_Types__double2float_01 extends AbstractTestCase
{
    public void bad() throws Throwable
    {

        BufferedReader readerBuffered = null;
        InputStreamReader readerInputStream = null;

        try
        {
            /* Enter: 1e-50, result should be 0.0 (for bad case)
             *
             * Note: alternate input
             * 999999999999999999999999999999999999999999999999999999999999999
             */

            readerInputStream = new InputStreamReader(System.in, "UTF-8");
            readerBuffered = new BufferedReader(readerInputStream);
            double doubleNumber = 0;

            IO.writeString("Enter double number (1e-50): ");

            try
            {
                doubleNumber = Double.parseDouble(readerBuffered.readLine());
            }
            catch (NumberFormatException exceptionNumberFormat)
            {
                IO.writeLine("Error parsing number");
            }

            /* FLAW: should not cast without checking if conversion is safe */
            IO.writeLine("" + (float)doubleNumber);
        }
        catch (IOException exceptIO)
        {
            IO.logger.log(Level.WARNING, "Error with stream reading", exceptIO);
        }
        finally
        {
            try
            {
                if (readerBuffered != null)
                {
                    readerBuffered.close();
                }
            }
            catch (IOException exceptIO)
            {
                IO.logger.log(Level.WARNING, "Error closing BufferedReader", exceptIO);
            }

            try
            {
                if (readerInputStream != null)
                {
                    readerInputStream.close();
                }
            }
            catch (IOException exceptIO)
            {
                IO.logger.log(Level.WARNING, "Error closing InputStreamReader", exceptIO);
            }
        }

    }

    public void good() throws Throwable
    {
        good1();
    }

    private void good1() throws Throwable
    {

        BufferedReader readerBuffered = null;
        InputStreamReader readerInputStream = null;

        try
        {
            readerInputStream = new InputStreamReader(System.in, "UTF-8");
            readerBuffered = new BufferedReader(readerInputStream);
            double num = 0;

            IO.writeString("Enter double number (1e-50): ");

            try
            {
                num = Double.parseDouble(readerBuffered.readLine());
            }
            catch (NumberFormatException exceptionNumberFormat)
            {
                IO.writeLine("Error parsing number");
            }

            /* FIX: check for conversion error */
            if (num > Float.MAX_VALUE || num < Float.MIN_VALUE)
            {
                IO.writeLine("Error, cannot safely cast this number to a float!");
                return;
            }

            IO.writeLine("" + (float)num);
        }
        catch (IOException exceptIO)
        {
            IO.logger.log(Level.WARNING, "Error with stream reading", exceptIO);
        }
        finally
        {
            try
            {
                if (readerBuffered != null)
                {
                    readerBuffered.close();
                }
            }
            catch (IOException exceptIO)
            {
                IO.logger.log(Level.WARNING, "Error closing BufferedReader", exceptIO);
            }

            try
            {
                if (readerInputStream != null)
                {
                    readerInputStream.close();
                }
            }
            catch (IOException exceptIO)
            {
                IO.logger.log(Level.WARNING, "Error closing InputStreamReader", exceptIO);
            }
        }

    }

    /* Below is the main(). It is only used when building this testcase on
     * its own for testing or for building a binary to use in testing binary
     * analysis tools. It is not used when compiling all the testcases as one
     * application, which is how source code analysis tools are tested.
     */
    public static void main(String[] args) throws ClassNotFoundException,
           InstantiationException, IllegalAccessException
    {
        mainFromParent(args);
    }
}

