/* TEMPLATE GENERATED TESTCASE FILE
Filename: CWE190_Integer_Overflow__short_rand_add_51a.java
Label Definition File: CWE190_Integer_Overflow.label.xml
Template File: sources-sinks-51a.tmpl.java
*/
/*
 * @description
 * CWE: 190 Integer Overflow
 * BadSource: rand Set data to result of rand()
 * GoodSource: A hardcoded non-zero, non-min, non-max, even number
 * Sinks: add
 *    GoodSink: Ensure there will not be an overflow before adding 1 to data
 *    BadSink : Add 1 to data, which can cause an overflow
 * Flow Variant: 51 Data flow: data passed as an argument from one function to another in different classes in the same package
 *
 * */






public class CWE190_Integer_Overflow__short_rand_add_51a extends AbstractTestCase
{
    public void bad() throws Throwable
    {
        short data;

        /* POTENTIAL FLAW: Use a random value */
        data = (short)((new java.security.SecureRandom()).nextInt(1+Short.MAX_VALUE-Short.MIN_VALUE)+Short.MIN_VALUE);

        (new CWE190_Integer_Overflow__short_rand_add_51b()).badSink(data  );
    }

    public void good() throws Throwable
    {
        goodG2B();
        goodB2G();
    }

    /* goodG2B() - use goodsource and badsink */
    private void goodG2B() throws Throwable
    {
        short data;

        /* FIX: Use a hardcoded number that won't cause underflow, overflow, divide by zero, or loss-of-precision issues */
        data = 2;

        (new CWE190_Integer_Overflow__short_rand_add_51b()).goodG2BSink(data  );
    }

    /* goodB2G() - use badsource and goodsink */
    private void goodB2G() throws Throwable
    {
        short data;

        /* POTENTIAL FLAW: Use a random value */
        data = (short)((new java.security.SecureRandom()).nextInt(1+Short.MAX_VALUE-Short.MIN_VALUE)+Short.MIN_VALUE);

        (new CWE190_Integer_Overflow__short_rand_add_51b()).goodB2GSink(data  );
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
