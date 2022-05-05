/* TEMPLATE GENERATED TESTCASE FILE
Filename: CWE789_Uncontrolled_Mem_Alloc__PropertiesFile_ArrayList_53c.java
Label Definition File: CWE789_Uncontrolled_Mem_Alloc.int.label.xml
Template File: sources-sink-53c.tmpl.java
*/
/*
 * @description
 * CWE: 789 Uncontrolled Memory Allocation
 * BadSource: PropertiesFile Read data from a .properties file (in property named data)
 * GoodSource: A hardcoded non-zero, non-min, non-max, even number
 * Sinks: ArrayList
 *    BadSink : Create an ArrayList using data as the initial size
 * Flow Variant: 53 Data flow: data passed as an argument from one method through two others to a fourth; all four functions are in different classes in the same package
 *
 * */






public class CWE789_Uncontrolled_Mem_Alloc__PropertiesFile_ArrayList_53c
{
    public void badSink(int data ) throws Throwable
    {
        (new CWE789_Uncontrolled_Mem_Alloc__PropertiesFile_ArrayList_53d()).badSink(data );
    }

    /* goodG2B() - use goodsource and badsink */
    public void goodG2BSink(int data ) throws Throwable
    {
        (new CWE789_Uncontrolled_Mem_Alloc__PropertiesFile_ArrayList_53d()).goodG2BSink(data );
    }
}